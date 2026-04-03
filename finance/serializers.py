from rest_framework import serializers
from .models import Category,Record


from rest_framework import serializers
from .models import Category, Record


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'type']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Category name cannot be empty")
        return value

    def validate(self, data):
        name = data.get('name')
        type_ = data.get('type')

        if self.instance:
            exists = Category.objects.filter(name=name, type=type_).exclude(id=self.instance.id).exists()
        else:
            exists = Category.objects.filter(name=name, type=type_).exists()

        if exists:
            raise serializers.ValidationError({
                "category": "Category with this name and type already exists"
            })

        return data


class RecordSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Record
        fields = [
            'id',
            'user',
            'amount',
            'category',
            'date',
            'description',
            'created_at',
            'updated_at'
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value

    def validate(self, data):
        category = data.get('category')

        if category is None:
            raise serializers.ValidationError({
                "category": "Category is required"
            })

        return data
    

class RecordDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Record
        fields = [
            'id',
            'user',
            'amount',
            'category',
            'category_name',
            'date',
            'description',
            'created_at',
            'updated_at'
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value