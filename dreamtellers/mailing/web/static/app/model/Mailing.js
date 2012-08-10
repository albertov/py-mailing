Ext.define('WebMailing.model.Mailing', {
    extend: 'Ext.data.Model',
    idProperty: 'number',
    fields: [
        {name:'number', type: 'int'},
        {name:'date', type: 'date',  dateFormat: 'c'},
        {name:'created', type: 'date',  dateFormat: 'c'},
        {name:'modified', type: 'date',  dateFormat: 'c'}
    ],
    associations: [
        {type: 'hasMany', model: 'Item', foreignKey: 'mailing', name:'_items'}
    ],
    proxy: {
        type: 'rest',
        url: 'mailing/',
        reader: {
            type: 'json',
            root: 'mailings',
        }
    }
});
