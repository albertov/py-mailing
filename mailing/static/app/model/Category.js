Ext.define('Mailing.model.Category', {
    extend: 'Ext.data.Model',
    requires: [
        'Mailing.Rest'
    ],
    idProperty: 'id',
    fields: [
        {name:'id', type: 'int'},
        {name:'category_id', defaultValue:null},
        {name:'image_id', defaultValue:null},
        {name:'image_title', mapping:"image.title", persist:false},
        {name:'image_url', mapping:"image.internal_url", persist:false},
        {name:'title', type: 'string'},
        {name:'created', type: 'date',  dateFormat: 'c'},
        {name:'modified', type: 'date',  dateFormat: 'c'}
    ],
    hasMany: [
        {
            model: 'Mailing.model.Item',
            foreignKey: 'category_id',
            name: 'items',
            primaryKey:'id'
        }, {
            model: 'Mailing.model.Category',
            foreignKey: 'category_id',
            name: 'subcategories',
            primaryKey:'id'
        }
    ],
    belongsTo: [
        {
            model: 'Mailing.model.Category',
            foreignKey: 'category_id',
            primaryKey:'id',
            name: 'category',
            setterName: 'setCategory',
            getterName: 'getCategory'
        }, {
            model: 'Mailing.model.Image',
            foreignKey: 'image_id',
            primaryKey:'id',
            name: 'image',
            setterName: 'setImage',
            getterName: 'getImage'
        }
    ],
    proxy: {
        type: 'rest2',
        url: url('category/'),
        reader: {
            type: 'json',
            root: 'categories',
        }
    }
});

