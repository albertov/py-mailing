Ext.define('Mailing.model.MailingTemplate', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    requires: [
        'Mailing.Rest'
    ],
    fields: [
        {name:'id', persist:false},
        {name:'mailing_id', type: 'int'},
        {name:'template_id', type:'int'}
    ],
    belongsTo: [
        {
            model: 'Mailing.model.Mailing',
            foreignKey: 'mailing_id',
            name:'mailing',
            setterName: 'setMailing',
            getterName: 'getMailing'
        }, {
            model: 'Mailing.model.Template',
            foreignKey: 'template_id',
            name:'template',
            setterName: 'setTemplate',
            getterName: 'getTemplate'
        }
    ],
    proxy: {
        type: 'rest2',
        url: url('mailing_template/'),
        batchActions: true,
        reader: {
            type: 'json',
            root: 'mailing_templates'
        }
    }
});
