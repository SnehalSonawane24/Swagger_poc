from rest_framework import serializers
from app.models import Item

# Modelseializers    
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        
# seializers         
class ExampleSerialiser(serializers.Serializer):
    name = serializers.CharField(max_length = 100)
    description = serializers.CharField()
    
    def create(self, validated_data):
        return Item.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description =validated_data.get('description', instance.description)
        instance.save()
        return instance
    
class ExampleOutputSerialiser(serializers.Serializer):
    name = serializers.CharField(max_length = 100)
    id = serializers.IntegerField()
    
    class Meta:
        model = Item
        fields = ['id', 'name']
    
    