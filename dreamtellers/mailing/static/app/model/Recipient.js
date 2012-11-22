Ext.define('WebMailing.model.Recipient', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    requires: [
        'WebMailing.Rest'
    ],
    fields: [
        {name:'id', type: 'int'},
        {name:'name', type: 'string'},
        {name:'email', type: 'string'},
        {name:'group_id'},
        {name:'created', type: 'date',  dateFormat: 'c', persist:false},
        {name:'modified', type: 'date',  dateFormat: 'c', persist:false}
    ],
    proxy: {
        type: 'rest2',
        url: url('recipient/'),
        reader: {
            type: 'json',
            root: 'recipients'
        }
    }
});
