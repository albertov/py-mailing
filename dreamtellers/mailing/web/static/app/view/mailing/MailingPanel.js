Ext.define('WebMailing.view.mailing.MailingPanel', {
    extend: 'Ext.tab.Panel',
    alias: 'widget.mailingpanel',
    requires: [
        'WebMailing.view.mailing.MailingView'
    ],
    initComponent: function() {
        Ext.apply(this, {
            items: [
                {
                    xtype: 'mailingview',
                    title: 'Vista',
                    src: this.record.getViewUrl()
                }
            ]
        }),
        this.callParent(arguments);
    }
});
