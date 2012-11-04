Ext.define('WebMailing.view.mailing.Edit', {
    extend: 'Ext.panel.Panel',
    requires: [
        'WebMailing.view.item.Edit'
    ],
    alias: 'widget.mailing_edit',
    layout: 'fit',
    border: false,
    items: [
        {
            xtype: 'item_edit'
        }
    ],
    setRecord: function(record) {
        this.record = record;
        this.down('item_edit').setMailing(record);
    }
});
