Ext.define('WebMailing.model.SentMailing', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    requires: [
        'WebMailing.Rest',
        'WebMailing.model.GroupSentMailing'
    ],
    fields: [
        {name:'id', type: 'int'},
        {name:'mailing_id', type: 'int'},
        {name:'sent_date', type: 'date',  dateFormat: 'c'},
        {name:'programmed_date', type: 'date',  dateFormat: 'c'}
    ],
    belongsTo: [
        {
            model: 'WebMailing.model.Mailing',
            foreignKey: 'mailing_id',
            name:'mailing',
            setterName: 'setMailing',
            getterName: 'getMailing'
        }
    ],
    hasMany: [
        {
            model: 'WebMailing.model.GroupSentMailing',
            foreignKey: 'sent_mailing_id',
            name:'group_sent_mailings',
            primaryKey:'id'
        }
    ],
    proxy: {
        type: 'rest2',
        url: 'sent_mailing/',
        reader: {
            type: 'json',
            root: 'sent_mailings'
        }
    }
});