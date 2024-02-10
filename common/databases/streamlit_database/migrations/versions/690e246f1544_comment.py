"""comment

Revision ID: 690e246f1544
Revises: 
Create Date: 2024-02-10 05:18:21.617109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '690e246f1544'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False, comment='書籍名'),
    sa.Column('category', sa.String(length=255), nullable=False, comment='カテゴリ'),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('book_contents',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('book_id', sa.BigInteger(), nullable=False),
    sa.Column('sort', sa.Integer(), nullable=False, comment='順番'),
    sa.Column('title', sa.String(length=255), nullable=True, comment='章名'),
    sa.Column('content', mysql.LONGTEXT(), nullable=False, comment='内容'),
    sa.Column('file_name', sa.String(length=255), nullable=False, comment='ファイル名'),
    sa.Column('file_type', sa.String(length=255), nullable=False, comment='ファイルタイプ'),
    sa.Column('file_size', sa.Integer(), nullable=False, comment='ファイルサイズ'),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('book_content_summaries',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('book_content_id', sa.BigInteger(), nullable=False),
    sa.Column('content', mysql.LONGTEXT(), nullable=False, comment='内容'),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['book_content_id'], ['book_contents.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('book_content_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book_content_summaries')
    op.drop_table('book_contents')
    op.drop_table('books')
    # ### end Alembic commands ###