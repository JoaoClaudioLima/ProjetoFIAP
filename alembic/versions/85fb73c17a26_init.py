"""init

Revision ID: 85fb73c17a26
Create Date: 2024-12-28 15:02:52.420613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.utils.miscelaneous import generate_fake_user

# revision identifiers, used by Alembic.
revision: str = '85fb73c17a26'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # Criação da tabela de users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String, unique=True, index=True),
        sa.Column('email', sa.String, unique=True, index=True),
        sa.Column('full_name', sa.String),
        sa.Column('hashed_password', sa.String),
    )

    # Inserção de dados na tabela de users

    for i in range(5):
        fake_username, fake_email, fake_name, fake_password = generate_fake_user()
        sql_query = f"INSERT INTO users (username, email, full_name, hashed_password) VALUES ('{fake_username}', '{fake_email}', '{fake_name}', '{fake_password}')"
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
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    # Inserção de dados na tabela de tarefas
    op.execute(
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES "
        "('Tarefa 1', 'Descrição da tarefa 1', 1, 1), "
        "('Tarefa 2', 'Descrição da tarefa 2', 2, 1), "
        "('Tarefa 3', 'Descrição da tarefa 3', 3, 1)"
    )


def downgrade():
    # Remoção das tabelas
    op.drop_table('task_status')
    op.drop_table('users')
    op.drop_table('tasks')
