Ext.define('WebMailing.model.GroupSentMailing', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    requires: [
        'WebMailing.Rest'
    ],
    fields: [
        {name:'id', persist:false},
        {name:'group_id', type: 'int'},
        {name:'sent_mailing_id', type:'int'}
    ],
    belongsTo: [
        {
            model: 'WebMailing.model.Mailing',
            foreignKey: 'mailing_id',
            name:'mailing',
            setterName: 'setMailing',
            getterName: 'getMailing'
        }, {
            model: 'WebMailing.model.Group',
            foreignKey: 'group_id',
            name:'group',
            setterName: 'setGroup',
            getterName: 'getGroup'
        }
    ],
    proxy: {
        type: 'rest2',
        url: url('group_sent_mailing/'),
        batchActions: true,
        reader: {
            type: 'json',
            root: 'group_sent_mailings'
        }
    }
});
