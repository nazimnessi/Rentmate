import graphene
from graphql import GraphQLError
from payment.models import Payment
from datetime import datetime

from payment.node import PaymentType, PaymentInput


class AddPayment(graphene.Mutation):
    class Arguments:
        payment = PaymentInput(required=True)

    payment = graphene.Field(PaymentType)

    @staticmethod
    def mutate(self, info, payment=None):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("User not authenticated")
        payment['payee'] = user
        payment['transaction_date'] = datetime.strptime(payment["transaction_date"], "%Y-%m-%d")
        payment_instance = Payment.objects.create(**payment)
        return AddPayment(payment=payment_instance)


class Mutation(graphene.ObjectType):
    add_payment = AddPayment.Field()
