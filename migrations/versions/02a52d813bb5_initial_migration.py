"""Initial migration

Revision ID: 02a52d813bb5
Revises: 
Create Date: 2022-07-29 18:42:25.816252

"""
from alembic import op
import flask_bcrypt
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02a52d813bb5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # # ### commands auto generated by Alembic - please adjust! ###
    # op.alter_column('saved_job', 'username',
    #            existing_type=sa.VARCHAR(),
    #            nullable=False)
    # # ### end Alembic commands ###

    # delete all existing data in the tables
    op.execute("DELETE FROM saved_job;")
    op.execute("DELETE FROM user;")
    
    # start recording job_id with each saved job
    op.add_column('saved_job',
        sa.Column('job_id', sa.String())
    )

    # represent the user table in jobify.db as a Python object
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect(only=('user',))
    user = sa.Table('user', meta)

    # create dummy users
    op.bulk_insert(
        user,
        [
            {'id': 1, 'username': 'test1',
                'password': flask_bcrypt.generate_password_hash('abc')},
            {'id': 2, 'username': 'test2',
                'password': flask_bcrypt.generate_password_hash('123')},
            {'id': 3, 'username': 'test3',
                'password': flask_bcrypt.generate_password_hash('abc123')},
            {'id': 4, 'username': 'test4',
                'password': flask_bcrypt.generate_password_hash('123abc')}
        ]
    )


def downgrade():
    # # ### commands auto generated by Alembic - please adjust! ###
    # op.alter_column('saved_job', 'username',
    #            existing_type=sa.VARCHAR(),
    #            nullable=True)
    # # ### end Alembic commands ###
    
    # Delete job_id from each saved job (cannot recover data if we go back!)
    op.drop_column('saved_job', 'job_id')

    # Remove dummy users
    op.execute("DELETE FROM user WHERE username='test1' OR username='test2' OR username='test3' OR username='test4';")