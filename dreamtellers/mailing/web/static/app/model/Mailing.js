Ext.define('WebMailing.model.Mailing', {
    extend: 'Ext.data.Model',
    fields: [
        {name:'number', type: 'int'},
        {name:'date', type: 'date',  dateFormat: 'c'}
    ],
    proxy: {
        type: 'ajax',
        url: 'mailing/',
        reader: {
            type: 'json',
            root: 'mailings',
            idProperty: 'number'
        }
    }
});
