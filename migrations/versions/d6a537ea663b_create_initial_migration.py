"""Add content_hash to bazels

Revision ID: d6a537ea663b
Revises: 5cfa69fff879
Create Date: 2024-05-13 12:43:14.295352

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d6a537ea663b"
down_revision: Union[str, None] = "5cfa69fff879"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "bazels", sa.Column("content_hash", sa.String(length=64), nullable=True)
    )
    op.create_unique_constraint("bazels_content_hash_key", "bazels", ["content_hash"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("bazels_content_hash_key", "bazels", type_="unique")
    op.drop_column("bazels", "content_hash")
    # ### end Alembic commands ###