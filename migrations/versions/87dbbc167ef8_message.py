"""message

Revision ID: 87dbbc167ef8
Revises: 4192b0e96741
Create Date: 2024-06-29 16:56:44.586893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87dbbc167ef8'
down_revision = '4192b0e96741'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(op.f('fk_restaurant_pizzas_pizza_id_pizzas'), 'restaurant_pizzas', 'pizzas', ['pizza_id'], ['id'])
    op.create_foreign_key(op.f('fk_restaurant_pizzas_restaurant_id_restaurants'), 'restaurant_pizzas', 'restaurants', ['restaurant_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_restaurant_pizzas_restaurant_id_restaurants'), 'restaurant_pizzas', type_='foreignkey')
    op.drop_constraint(op.f('fk_restaurant_pizzas_pizza_id_pizzas'), 'restaurant_pizzas', type_='foreignkey')
    op.drop_column('restaurant_pizzas', 'pizza_id')
    op.drop_column('restaurant_pizzas', 'restaurant_id')
    # ### end Alembic commands ###
