Ext.define('WebMailing.model.Item', {
    extend: 'Ext.data.Model',
    requires: [
        'WebMailing.Rest',
        'WebMailing.model.Category'
    ],
    idProperty: 'id',
    fields: [
        {name:'id'},
        {name:'title', type: 'string'},
        {name:'content', type: 'string', defaultValue:null},
        {name:'url', type: 'string', defaultValue:null},
        {name:'type', type: 'string'},
        {name:'position', type: 'int'},
        {name:'created', type: 'date',  dateFormat: 'c'},
        {name:'modified', type: 'date',  dateFormat: 'c'},
        {name:'category_id', defaultValue:null},
        {name:'mailing_id', defaultValue:null},
        {name:'image_id', defaultValue:null}
    ],
    belongsTo: [
        {
            model: 'WebMailing.model.Mailing',
            foreignKey: 'mailing_id',
            name:'mailing',
            setterName: 'setMailing',
            getterName: 'getMailing'
        }, {
            model: 'WebMailing.model.Category',
            foreignKey: 'category_id',
            primaryKey:'id',
            name:'category',
            setterName: 'setCategory',
            getterName: 'getCategory'
        }
    ],
    proxy: {
        type: 'rest2',
        url: url('item/'),
        batchActions: true,
        reader: {
            type: 'json',
            root: 'items',
        }
    }
});

