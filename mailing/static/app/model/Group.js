Ext.define('Mailing.model.Group', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    requires: [
        'Mailing.Rest'
    ],
    fields: [
        {name:'id', type: 'int'},
        {name:'name', type: 'string'},
        {name:'description', type: 'string'},
        {name:'priority', type: 'int'},
        {name:'created', type: 'date',  dateFormat: 'c', persist:false},
        {name:'modified', type: 'date',  dateFormat: 'c', persist:false}
    ],
    proxy: {
        type: 'rest2',
        url: url('group/'),
        reader: {
            type: 'json',
            root: 'groups'
        }
    }
});
