Ext.define('Mailing.model.MailingDelivery', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    requires: [
        'Mailing.Rest',
        'Mailing.model.GroupMailingDelivery'
    ],
    fields: [
        {name:'id', type: 'int'},
        {name:'mailing_id', type: 'int'},
        {name:'sent_date', type: 'date',  dateFormat: 'c', persist:false},
        {name:'programmed_date', type: 'date',  dateFormat: 'c'},
        {name:'created', type: 'date',  dateFormat: 'c', persist:false},
        {name:'modified', type: 'date',  dateFormat: 'c', persist:false}
    ],
    belongsTo: [
        {
            model: 'Mailing.model.Mailing',
            foreignKey: 'mailing_id',
            name:'mailing',
            setterName: 'setMailing',
            getterName: 'getMailing'
        }
    ],
    hasMany: [
        {
            model: 'Mailing.model.GroupMailingDelivery',
            foreignKey: 'mailing_delivery_id',
            name:'group_mailing_deliveries',
            primaryKey:'id',
            storeConfig: {
                autoSync: true
            }
        }
    ],
    proxy: {
        type: 'rest2',
        url: url('mailing_delivery/'),
        reader: {
            type: 'json',
            root: 'mailing_deliveries'
        }
    }
});
