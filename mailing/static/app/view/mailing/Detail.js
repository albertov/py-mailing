Ext.define('Mailing.view.mailing.Detail', {
    extend: 'Ext.tab.Panel',
    requires: [
        'Mailing.view.mailing.Edit',
        'Mailing.view.mailing.View',
        'Mailing.view.mailing_delivery.Panel'
    ],
    alias: 'widget.mailing_detail',
    title: '&nbsp;',
    record: null,
    disabled: true,
    items: [
        {
            itemId: 'view',
            xtype: 'tabpanel',
            title: 'Vista', // i18n
            items: [
                {
                    itemId: 'html_view',
                    xtype: 'mailing_view',
                    view_type: 'xhtml',
                    title: 'HTML' // i18n
                }, {
                    itemId: 'text_view',
                    xtype: 'mailing_view',
                    view_type: 'text',
                    title: 'Texto' // i18n
                }
            ]
        }, {
            itemId: 'edit',
            xtype: 'mailing_edit',
            title: 'Edición' //i18n
        }, {
            itemId: 'mailing_deliveries',
            xtype: 'mailing_deliveries',
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
            this.down('#edit').setRecord(this.record);
            this.down('#mailing_deliveries').setRecord(this.record);
            this.down('#html_view').setRecord(this.record);
            this.down('#text_view').setRecord(this.record);
            this.setTitle(this.record.getTitle());
        }
    }
});
