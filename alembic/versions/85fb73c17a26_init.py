"""init

Revision ID: 85fb73c17a26
Revises: 49b338b4b37f
Create Date: 2024-12-28 15:02:52.420613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85fb73c17a26'
down_revision: Union[str, None] = '49b338b4b37f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
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
        sa.Column('scriprion', sa.Text, nullable=True),
        sa.Column('status_id', sa.Integer, sa.ForeignKey('status.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

    # Inserção de dados na tabela de tarefas
    op.execute(
        "INSERT INTO tasks (titulo, descricao, status_id) VALUES "
        "('Tarefa 1', 'Descrição da tarefa 1', 1), "
        "('Tarefa 2', 'Descrição da tarefa 2', 2), "
        "('Tarefa 3', 'Descrição da tarefa 3', 3)"
    )


def downgrade():
    # Remoção das tabelas
    op.drop_table('tasks')
    op.drop_table('task_status')
