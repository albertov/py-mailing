Ext.define('WebMailing.model.Template', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    requires: [
        'WebMailing.Rest'
    ],
    fields: [
        {name:'id', type: 'int'},
        {name:'title', type: 'string'},
        {name:'type', type: 'string'},
        {name:'body', type: 'string'},
        {name:'created', type: 'date',  dateFormat: 'c', persist:false},
        {name:'modified', type: 'date',  dateFormat: 'c', persist:false}
    ],
    proxy: {
        type: 'rest2',
        url: url('template/'),
        reader: {
            type: 'json',
            root: 'templates'
        },
        writer: {
            type: 'json',
            writeAllFields: true
        }
    }
});
