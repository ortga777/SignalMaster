class MLModel(Base):
    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    version = Column(String(50), nullable=False)
    model_path = Column(String(255), nullable=False)
    accuracy = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    model_parameters = Column(Text)  # ← LINHA 141 CORRIGIDA    model_parameters = Column(Text)

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), nullable=False)
    trade_type = Column(String(20), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="executed")

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    signal_id = Column(Integer, ForeignKey("signals.id"))
    broker_id = Column(Integer, ForeignKey("user_brokers.id"))

    # Relationships
    user = relationship("User")
    signal = relationship("Signal")
    broker = relationship("UserBroker")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(100), nullable=False)
    resource = Column(String(100), nullable=False)
    resource_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    old_values = Column(Text)
    new_values = Column(Text)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")    model_parameters = Column(Text)  # Corrigido: era 'parameters'

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), nullable=False)
    trade_type = Column(String(20), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime(time    model_parameters = Column(Text)  # Mudei de 'parameters' para 'model_parameters'

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), nullable=False)
    trade_type = Column(String(20), nullable=False)  # buy, sell
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="executed")  # pending, executed, cancelled, failed

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    signal_id = Column(Integer, ForeignKey("signals.id"))
    broker_id = Column(Integer, ForeignKey("user_brokers.id"))

    # Relationships
    user = relationship("User")
    signal = relationship("Signal")
    broker = relationship("UserBroker")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(100), nullable=False)
    resource = Column(String(100), nullable=False)
    resource_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    old_values = Column(Text)  # JSON string
    new_values = Column(Text)  # JSON string
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")    parameters = Column(Text)  # JSON string with model parameters

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), nullable=False)
    trade_type = Column(String(20), nullable=False)  # buy, sell
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="executed")  # pending, executed, cancelled, failed

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    signal_id = Column(Integer, ForeignKey("signals.id"))
    broker_id = Column(Integer, ForeignKey("user_brokers.id"))

    # Relationships
    user = relationship("User")
    signal = relationship("Signal")
    broker = relationship("UserBroker")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(100), nullable=False)
    resource = Column(String(100), nullable=False)
    resource_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    old_values = Column(Text)  # JSON string
    new_values = Column(Text)  # JSON string
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
