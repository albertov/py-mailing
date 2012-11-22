Ext.define('Mailing.view.template.Detail', {
    extend: 'Ext.panel.Panel',
    requires: [
        'Mailing.view.template.Form'
    ],
    alias: 'widget.template_detail',
    layout: 'fit',
    record: null,
    disabled: true,
    items: {
        itemId: 'form',
        title: '&nbsp;',
        xtype: 'template_form'
    },
    setRecord: function(record) {
        this.record = record;
        this.enable();
        this.items.get('form').getForm().loadRecord(record);
        this.items.get('form').setTitle(record.get('title'));
    },
    getRecord: function() {
        return this.record;
    }
});
