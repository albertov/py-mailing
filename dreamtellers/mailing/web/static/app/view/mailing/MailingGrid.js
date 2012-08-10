Ext.define('WebMailing.view.mailing.MailingGrid', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.mailinggrid',
    store: 'Mailings',
    columns: [
        {text: 'Número', dataIndex: 'number', sortable: true},
        {text: 'Fecha', dataIndex: 'date', sortable: true,
         renderer: Ext.util.Format.dateRenderer('Y/m/d')}
    ],
    listeners: {
        afterrender: function() {
            this.store.load();
        }
    }
});
