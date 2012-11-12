Ext.define('WebMailing.view.template.Detail', {
    extend: 'Ext.panel.Panel',
    requires: [
        'WebMailing.view.template.Form'
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
