import graphene
from graphql import GraphQLError
from payment.models import Payment
from datetime import datetime

from payment.node import PaymentType, PaymentInput
from django.db import transaction


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


class MarkAsPaid(graphene.Mutation):
    class Arguments:
        payment = graphene.ID(required=True)
        status = graphene.Boolean(required=True)

    payment = graphene.Field(PaymentType)

    @staticmethod
    def mutate(self, info, payment=None, status=None):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("User not authenticated")
        payment_instance = Payment.objects.filter(id=payment).first()
        update_content = {
            "transaction_date": datetime.now(),
            "status": "Paid" if status else None if payment_instance.is_expense else "Pending",
            "mark_as_paid": status,
        }
        payment_instance, created = Payment.objects.update_or_create(
            id=payment, defaults=update_content
        )
        return MarkAsPaid(payment=payment_instance)


class DeletePayment(graphene.Mutation):
    class Arguments:
        payment_id = graphene.ID(required=True)
    status = graphene.Boolean()

    @staticmethod
    def mutate(root, info, payment_id=None):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("User not authenticated")
        try:
            with transaction.atomic():
                payment_instance = Payment.objects.get(id=payment_id)
                utility = payment_instance.utility
                if utility:
                    utility.delete()
                payment_instance.delete()
        except Payment.DoesNotExist:
            raise GraphQLError('Selected payment does not exist')
        except Exception as exe:
            transaction.rollback()
            raise GraphQLError(str(exe))
        return DeletePayment(status=True)


class Mutation(graphene.ObjectType):
    add_payment = AddPayment.Field()
    mark_as_paid = MarkAsPaid.Field()
    delete_payment = DeletePayment.Field()
