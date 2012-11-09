Ext.define('WebMailing.view.recipient.Grid', {
    extend: 'Ext.grid.Panel',
    requires: [
        'WebMailing.CRUDPlugin',
        'Ext.form.TextField'
    ],
    plugins: [
        {
            ptype: 'crud',
            actions: 'new,delete'
        }
    ],
    alias: 'widget.recipient_grid',
    store: 'Recipients',
    actions: 'new,delete',
    columns: [
        {
            text: 'Nombre',
            dataIndex: 'name',
            sortable: true,
            width: 350,
            field: {
                xtype: 'textfield',
                allowBlank: false
            }
        }, {
            text: 'Email',
            dataIndex: 'email',
            sortable: true,
            width: 350,
            field: {
                xtype: 'textfield',
                allowBlank: false,
                vtype: 'email'
            }
        }, {
            text: 'Group',
            dataIndex: 'group_id',
            sortable: true,
            width: 100,
            renderer: function(id) {
                if (id!==null) {
                    var g = Ext.getStore('Groups').getById(id);
                    if (g) {
                        return g.get('name');
                    }
                }
                return '';
            },
            field: {
                xtype: 'combo',
                store: 'Groups',
                valueField: 'id',
                displayField: 'name'
            }
        }, {
            text: 'Modificado',
            dataIndex: 'modified',
            sortable: true,
            renderer: Ext.util.Format.dateRenderer('Y/m/d H:i:s'),
            width:150
        }, {
            text: 'Creado',
            dataIndex: 'created',
            sortable: true,
            renderer: Ext.util.Format.dateRenderer('Y/m/d H:i:s'),
            width: 150
        }
    ],
    initComponent: function() {
        Ext.getStore('Groups').load();
        this.callParent(arguments);
    }
});
