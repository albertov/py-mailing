Ext.define('WebMailing.view.mailing.Detail', {
    extend: 'Ext.tab.Panel',
    requires: [
        'WebMailing.view.mailing.Edit',
        'WebMailing.view.mailing.View'
    ],
    alias: 'widget.mailing_detail',
    title: '&nbsp;',
    record: null,
    items: [
        {
            xtype: 'mailing_view',
            title: 'Vista' // i18n
        }, {
            xtype: 'mailing_edit',
            title: 'Edición' //i18n
        }
    ],
    setRecord: function(record) {
        this.record = record;
        this.items.get(0).setSrc(this.record.getViewUrl());
        this.items.get(1).setRecord(this.record);
        this.setTitle(
            Ext.String.format("Mailing #{0}", this.record.get('number')));
    }
});
