Ext.define('WebMailing.view.mailing.MailingGrid', {
    extend: 'Ext.grid.Panel',
    title: 'Envíos', // i18n
    alias: 'widget.mailinggrid',
    store: 'Mailings',
    columns: [
        {text: 'Número', dataIndex: 'number', sortable: true},
        {text: 'Fecha', dataIndex: 'date', sortable: true,
         renderer: Ext.util.Format.dateRenderer('Y/m/d')},
        {text: 'Creado', dataIndex: 'created', sortable: true,
         renderer: Ext.util.Format.dateRenderer('Y/m/d H:i:s'),
         width: 100},
        {text: 'Modificado', dataIndex: 'modified', sortable: true,
         renderer: Ext.util.Format.dateRenderer('Y/m/d H:i:s'),
         width:100}
    ],
    listeners: {
        afterrender: function() {
            this.store.load();
        }
    }
});
