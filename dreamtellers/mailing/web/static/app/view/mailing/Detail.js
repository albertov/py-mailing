Ext.define('WebMailing.view.mailing.Detail', {
    extend: 'Ext.tab.Panel',
    requires: [
        'WebMailing.view.mailing.Edit',
        'WebMailing.view.mailing.View',
        'WebMailing.view.sent_mailing.Panel'
    ],
    alias: 'widget.mailing_detail',
    title: '&nbsp;',
    record: null,
    disabled: true,
    items: [
        {
            itemId: 'view',
            xtype: 'mailing_view',
            title: 'Vista' // i18n
        }, {
            itemId: 'edit',
            xtype: 'mailing_edit',
            title: 'Edición' //i18n
        }, {
            itemId: 'sent_mailings',
            xtype: 'sent_mailings',
            title: 'Envíos' //i18n
        }
    ],
    setRecord: function(record) {
        this.record = record;
        this.refresh();
    },
    getRecord: function() {
        return this.record;
    },
    refresh: function() {
        if (this.record) {
            this.items.get('edit').setRecord(this.record);
            this.items.get('sent_mailings').setRecord(this.record);
            this.items.get('view').setSrc(this.record.getViewUrl());
            this.setTitle(this.record.getTitle());
        }
    }
});
