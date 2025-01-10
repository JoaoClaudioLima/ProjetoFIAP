"""init

Revision ID: d35bd14dea92
Revises: 
Create Date: 2024-12-29 16:47:24.511510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.utils.miscelaneous import hash_password
from src.utils.task import db_create_fake_task
from src.utils.user import db_generate_fake_user

# revision identifiers, used by Alembic.
revision: str = 'd35bd14dea92'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    users_ammount = 8

    # Criação da tabela de users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('is_admin', sa.Boolean, index=True, server_default=sa.sql.expression.false()),
        sa.Column('username', sa.String, unique=True, index=True),
        sa.Column('email', sa.String, unique=True, index=True),
        sa.Column('full_name', sa.String, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), index=True),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), index=True),
        sa.Column('deleted_at', sa.DateTime, nullable=True, index=True),
    )

    # Inserção de dados na tabela de users
    fake_password = hash_password('12345')
    op.execute(f"INSERT INTO users (is_admin, username, email, full_name, hashed_password) VALUES (True, 'j.lima', 'joao.lima@fakemail.com', 'Joao Lima', '{fake_password}')")
    op.execute(f"INSERT INTO users (is_admin, username, email, full_name, hashed_password) VALUES (False, 'j.clima', 'joao.clima@fakemail.com', 'Joao Clima', '{fake_password}')")
    for i in range(2, users_ammount + 1):
        fake_username, fake_email, fake_name, fake_hashed_password = db_generate_fake_user()
        sql_query = f"INSERT INTO users (is_admin, username, email, full_name, hashed_password) VALUES (False, '{fake_username}', '{fake_email}', '{fake_name}', '{fake_hashed_password}')"
        op.execute(sql_query)

    # Criação da tabela de status
    op.create_table(
        'task_status',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False)
    )

    # Inserção de dados na tabela de status
    op.execute(
        "INSERT INTO task_status (name) VALUES ('To Do'), ('In Progress'), ('Done')"
    )

    # Criação da tabela de tarefas
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('status_id', sa.Integer, sa.ForeignKey('task_status.id'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), index=True),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), index=True),
        sa.Column('deleted_at', sa.DateTime, nullable=True, index=True),
    )

    # Inserção de dados na tabela de tarefas
    for i in range(10):
        fake_title, fake_description, fake_status_id, fake_user_id = db_create_fake_task(i, users_ammount)
        sql_query = f"INSERT INTO tasks (title, description, status_id, user_id) VALUES ('{fake_title}', '{fake_description}', '{fake_status_id}', '{fake_user_id}')"
        op.execute(sql_query)


def downgrade():
    # Remoção das tabelas
    op.drop_table('tasks')
    op.drop_table('task_status')
    op.drop_table('users')
