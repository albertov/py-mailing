Ext.define('Mailing.model.Image', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    requires: [
        'Mailing.Rest'
    ],
    fields: [
        {name:'id', type: 'int'},
        {name:'title', type: 'string'},
        {name:'filename', type: 'string'},
        {name:'content_type', type: 'string', persist:false},
        {name:'url', type: 'string', persist:false, mapping:'internal_url'},
        {name:'created', type: 'date',  dateFormat: 'c', persist:false},
        {name:'modified', type: 'date',  dateFormat: 'c', persist:false}
    ],
    proxy: {
        type: 'rest2',
        url: url('image/'),
        reader: {
            type: 'json',
            root: 'images'
        }
    }
});
