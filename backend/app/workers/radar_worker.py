import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.celery_app import celery_app
from app.db.session import async_session_maker
from app.models.perfil import PerfilDeInteresse
from app.models.notification import Notification
from app.models.user import User
from app.services.pncp_service import search_opportunities
from app.services.email_service import send_email

async def _monitor_opportunities_async():
    async with async_session_maker() as session:
        result = await session.execute(select(PerfilDeInteresse))
        perfis = result.scalars().all()

        for perfil in perfis:
            print(f"Monitoring opportunities for profile: {perfil.nome_perfil}")
            opportunities = await search_opportunities(perfil)

            # Fetch the user associated with the profile to get their email
            user_result = await session.execute(select(User).filter(User.id == perfil.user_id))
            user = user_result.scalars().first()
            if not user:
                print(f"User not found for profile {perfil.nome_perfil}. Skipping notifications.")
                continue

            for opportunity in opportunities:
                pncp_id = opportunity.get("id") # Assumindo que a oportunidade tem um ID do PNCP
                if not pncp_id:
                    continue

                # Verificar se já foi notificado para este perfil e oportunidade
                notification_exists = await session.execute(
                    select(Notification).filter(
                        Notification.profile_id == perfil.id,
                        Notification.numero_controle_pncp == pncp_id
                    )
                )
                if notification_exists.scalars().first():
                    print(f"Opportunity {pncp_id} already notified for profile {perfil.nome_perfil}")
                    continue

                # Enviar notificação
                if perfil.notificacao_email and user.email:
                    subject = f"Nova Oportunidade no PNCP para {perfil.nome_perfil}"
                    body = f"Foi encontrada uma nova oportunidade no PNCP:\n\nObjeto: {opportunity.get('objetoContratacao', 'N/A')}\nLink: {opportunity.get('linkPNCP', 'N/A')}\n\nDetalhes do Perfil:\nNome: {perfil.nome_perfil}\nPalavras-chave: {perfil.palavras_chave}\nUF: {perfil.uf or 'N/A'}\nMunicípio IBGE: {perfil.municipio_ibge or 'N/A'}\nModalidade: {perfil.modalidade_contratacao or 'N/A'}\nCategoria: {perfil.categoria or 'N/A'}\nPrioridade: {perfil.prioridade_urgencia or 'N/A'}"
                    await send_email(user.email, subject, body)

                if perfil.notificacao_push:
                    print(f"Sending push notification for {perfil.nome_perfil} - {pncp_id}")
                    # TODO: Implement push notification logic (e.g., FCM)

                # Registrar notificação no DB
                notification = Notification(
                    user_id=perfil.user_id,
                    profile_id=perfil.id,
                    numero_controle_pncp=pncp_id,
                    tipo="email" if perfil.notificacao_email else "push", # Definir o tipo de notificação
                    sent_email=perfil.notificacao_email,
                    sent_push=perfil.notificacao_push,
                )
                session.add(notification)
                await session.commit()
                await session.refresh(notification)
                print(f"Notification recorded for {perfil.nome_perfil} - {pncp_id}")

@celery_app.task
def monitor_opportunities():
    asyncio.run(_monitor_opportunities_async())