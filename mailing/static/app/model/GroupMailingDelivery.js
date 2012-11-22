Ext.define('Mailing.model.GroupMailingDelivery', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    requires: [
        'Mailing.Rest'
    ],
    fields: [
        {name:'id', persist:false},
        {name:'group_id', type: 'int'},
        {name:'mailing_delivery_id', type:'int'}
    ],
    belongsTo: [
        {
            model: 'Mailing.model.Mailing',
            foreignKey: 'mailing_id',
            name:'mailing',
            setterName: 'setMailing',
            getterName: 'getMailing'
        }, {
            model: 'Mailing.model.Group',
            foreignKey: 'group_id',
            name:'group',
            setterName: 'setGroup',
            getterName: 'getGroup'
        }
    ],
    proxy: {
        type: 'rest2',
        url: url('group_mailing_delivery/'),
        batchActions: true,
        reader: {
            type: 'json',
            root: 'group_mailing_deliveries'
        }
    }
});
