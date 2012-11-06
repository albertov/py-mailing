Ext.define('WebMailing.model.Group', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    requires: [
        'WebMailing.Rest'
    ],
    fields: [
        {name:'id', type: 'int'},
        {name:'name', type: 'string'},
        {name:'description', type: 'string'},
        {name:'created', type: 'date',  dateFormat: 'c', persist:false},
        {name:'modified', type: 'date',  dateFormat: 'c', persist:false}
    ],
    proxy: {
        type: 'rest2',
        url: 'group/',
        reader: {
            type: 'json',
            root: 'groups'
        }
    }
});
