from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.core.database import License, User
from app.core.config import settings
from datetime import datetime, timedelta
import secrets
import string
from typing import Dict, Optional

class LicenseService:
    def __init__(self):
        self.license_types = {
            "monthly": timedelta(days=30),
            "quarterly": timedelta(days=90),
            "yearly": timedelta(days=365),
            "lifetime": None  # No expiration
        }
        
        self.license_features = {
            "monthly": {
                "ai_signals": True,
                "premium_pairs": True,
                "advanced_analytics": True,
                "api_access": True,
                "max_signals_per_day": 50
            },
            "quarterly": {
                "ai_signals": True,
                "premium_pairs": True,
                "advanced_analytics": True,
                "api_access": True,
                "max_signals_per_day": 100,
                "priority_support": True
            },
            "yearly": {
                "ai_signals": True,
                "premium_pairs": True,
                "advanced_analytics": True,
                "api_access": True,
                "max_signals_per_day": 200,
                "priority_support": True,
                "custom_indicators": True
            },
            "lifetime": {
                "ai_signals": True,
                "premium_pairs": True,
                "advanced_analytics": True,
                "api_access": True,
                "max_signals_per_day": 500,
                "priority_support": True,
                "custom_indicators": True,
                "whitelabel": True
            }
        }
    
    def generate_license_key(self) -> str:
        """Gera uma chave de licença única"""
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(16))
    
    async def create_license(self, db: AsyncSession, user_id: int, license_type: str) -> License:
        """Cria uma nova licença para o usuário"""
        if license_type not in self.license_types:
            raise ValueError(f"Tipo de licença inválido: {license_type}")
        
        # Gerar chave única
        license_key = self.generate_license_key()
        
        # Calcular datas
        start_date = datetime.utcnow()
        end_date = None
        
        if license_type != "lifetime":
            end_date = start_date + self.license_types[license_type]
        
        # Criar licença
        license = License(
            user_id=user_id,
            license_key=license_key,
            license_type=license_type,
            start_date=start_date,
            end_date=end_date,
            features=self.license_features[license_type],
            status="active"
        )
        
        db.add(license)
        await db.commit()
        await db.refresh(license)
        
        return license
    
    async def validate_license(self, db: AsyncSession, user_id: int) -> Dict:
        """Valida se o usuário tem uma licença ativa"""
        result = await db.execute(
            select(License).where(
                and_(
                    License.user_id == user_id,
                    License.status == "active"
                )
            )
        )
        license = result.scalar()
        
        if not license:
            return {
                "valid": False,
                "message": "Nenhuma licença ativa encontrada",
                "features": {}
            }
        
        # Verificar se a licença expirou
        if license.license_type != "lifetime" and license.end_date < datetime.utcnow():
            license.status = "expired"
            await db.commit()
            
            return {
                "valid": False,
                "message": "Licença expirada",
                "features": {}
            }
        
        return {
            "valid": True,
            "license": license,
            "features": license.features,
            "days_remaining": (license.end_date - datetime.utcnow()).days if license.end_date else None
        }
    
    async def get_license_price(self, license_type: str) -> float:
        """Retorna o preço do tipo de licença"""
        prices = {
            "monthly": settings.MONTHLY_PRICE,
            "quarterly": settings.QUARTERLY_PRICE,
            "yearly": settings.YEARLY_PRICE,
            "lifetime": settings.LIFETIME_PRICE
        }
        
        return prices.get(license_type, 0.0)
    
    async def upgrade_license(self, db: AsyncSession, user_id: int, new_license_type: str) -> License:
        """Faz upgrade da licença do usuário"""
        # Validar licença atual
        current_license = await self.validate_license(db, user_id)
        
        if current_license["valid"]:
            # Desativar licença atual
            current_license["license"].status = "upgraded"
        
        # Criar nova licença
        return await self.create_license(db, user_id, new_license_type)

license_service = LicenseService()
