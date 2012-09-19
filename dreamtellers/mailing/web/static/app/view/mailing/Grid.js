Ext.define('WebMailing.view.mailing.Grid', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.mailing_grid',
    store: 'Mailings',
    columns: [
        {text: 'Número', dataIndex: 'number', sortable: true},
        {text: 'Fecha', dataIndex: 'date', sortable: true,
         renderer: Ext.util.Format.dateRenderer('Y/m/d')},
        {text: 'Modificado', dataIndex: 'modified', sortable: true,
         renderer: Ext.util.Format.dateRenderer('Y/m/d H:i:s'),
         width:100},
        {text: 'Creado', dataIndex: 'created', sortable: true,
         renderer: Ext.util.Format.dateRenderer('Y/m/d H:i:s'),
         width: 100}
    ]
});
