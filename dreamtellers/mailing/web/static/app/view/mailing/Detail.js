Ext.define('WebMailing.view.mailing.Detail', {
    extend: 'Ext.tab.Panel',
    requires: [
        'WebMailing.view.mailing.View'
    ],
    alias: 'widget.mailing_detail',
    record: null,
    items: [
        {
            xtype: 'mailing_view',
            title: 'Vista'
        }, {
            xtype: 'panel',
            title: 'Edición'
        }
    ],
    setRecord: function(record) {
        this.record = record;
        this.items.get(0).setSrc(this.record.getViewUrl())
    }
});
