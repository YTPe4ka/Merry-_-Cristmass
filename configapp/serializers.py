from rest_framework import serializers
from .models import Category, Product, Supplier, Todo, User
from django.contrib.auth import authenticate
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class EmailRegisterserializer(serializers.Serializer):
    email = serializers.EmailField()
#///////////
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Username yoki password xato!")

#///////////    

class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

class TodoSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Todo
        fields = '__all__'
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['first_name', 'password', 'email','last_name','username','avatar','bio']
        
        def create(self, validated_data):
            # user = User.objects.create_user(
            #     username=validated_data['username'],
            #     email=validated_data['email'],
            #     password=validated_data['password'],
            #     first_name=validated_data.get('first_name', ''),
            #     last_name=validated_data.get('last_name', ''),
            # )
            # return user
            user = User(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name',  'email','last_name','username','avatar','bio')
        extra_kwargs = {'email': {'write_only': True}}





