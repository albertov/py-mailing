Ext.define('Mailing.view.recipient.Grid', {
    extend: 'Ext.grid.Panel',
    requires: [
        'Mailing.CRUDPlugin',
        'Ext.form.TextField',
        'Ext.form.field.Checkbox',
        'Ext.ux.grid.FiltersFeature'
    ],
    plugins: [
        {
            ptype: 'crud',
            item_names: ['Suscriptor', 'Suscriptores'],
            actions: 'new,delete'
        }
    ],
    features: [{ftype:'filters'}],
    alias: 'widget.recipient_grid',
    store: 'Recipients',
    actions: 'new,delete',
    columns: [
        {
            text: 'Nombre',
            dataIndex: 'name',
            sortable: true,
            filterable: true,
            width: 350,
            field: {
                xtype: 'textfield',
                allowBlank: false
            }
        }, {
            text: 'Email',
            dataIndex: 'email',
            sortable: true,
            filterable: true,
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
                displayField: 'name',
                editable: false,
                queryMode: 'local'
            }
        }, {
            text: 'Activo',
            dataIndex: 'active',
            sortable: true,
            filterable: true,
            width:40,
            renderer: Mailing.Util.renderBool,
            field: {
                xtype: 'checkbox'
            }
        }, {
            text: 'Estado',
            dataIndex: 'error',
            sortable: true,
            filterable: true,
            width:40,
            renderer: Mailing.Util.renderError
        }, {
            text: 'Modificado',
            dataIndex: 'modified',
            sortable: true,
            filterable: true,
            renderer: Ext.util.Format.dateRenderer('Y/m/d H:i:s'),
            width:150
        }, {
            text: 'Creado',
            dataIndex: 'created',
            sortable: true,
            filterable: true,
            renderer: Ext.util.Format.dateRenderer('Y/m/d H:i:s'),
            width: 150
        }
    ],
    initComponent: function() {
        Ext.getStore('Groups').load();
        this.callParent(arguments);
    }
});
