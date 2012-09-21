Ext.define('WebMailing.model.Category', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    fields: [
        {name:'id', type: 'int'},
        {name:'category_id', defaultValue:null},
        {name:'title', type: 'string'},
        {name:'created', type: 'date',  dateFormat: 'c'},
        {name:'modified', type: 'date',  dateFormat: 'c'}
    ],
    hasMany: [
        {
            model: 'WebMailing.model.Item',
            foreignKey: 'category_id',
            name: 'items',
            primaryKey:'id'
        }, {
            model: 'WebMailing.model.Category',
            foreignKey: 'category_id',
            name: 'subcategories',
            primaryKey:'id'
        }
    ],
    belongsTo: [
        {
            model: 'WebMailing.model.Category',
            foreignKey: 'category_id',
            primaryKey:'id',
            name: 'category',
            setterName: 'setCategory',
            getterName: 'getCategory'
        }
    ],
    proxy: {
        type: 'rest',
        url: 'category/',
        reader: {
            type: 'json',
            root: 'categories',
        }
    }
});

