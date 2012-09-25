Ext.define('WebMailing.view.mailing.Grid', {
    extend: 'Ext.grid.Panel',
    requires: [
        'Ext.grid.plugin.RowEditing',
        'Ext.form.TextField',
        'Ext.form.NumberField',
        'Ext.form.DateField',
    ],
    alias: 'widget.mailing_grid',
    store: 'Mailings',
    title: 'Envíos', //i18n
    columns: [
        {
            text: 'Número',
            dataIndex: 'number',
            sortable: true,
            field: {
                xtype: 'numberfield'
            }
        }, {
            text: 'Fecha',
            dataIndex: 'date',
            sortable: true,
            renderer: Ext.util.Format.dateRenderer('Y/m/d'),
            field: {
                xtype: 'datefield',
                format: 'Y/m/d'
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
        this.rowEditor = Ext.create('Ext.grid.plugin.RowEditing');
        this.plugins = [this.rowEditor];
        this.actions = {
            'new': Ext.create('Ext.Action', {
                text: 'Nuevo', //18n
                handler: Ext.bind(this.fireEvent, this, ['new_mailing', this])
            }),
            'delete': Ext.create('Ext.Action', {
                text: 'Eliminar', //18n
                disabled: true,
                handler: Ext.bind(this.fireEventWithRecord, this,
                                  ['delete_mailing'])
            }),
            'edit': Ext.create('Ext.Action', {
                text: 'Modificar', //18n
                disabled: true,
                handler: Ext.bind(this.fireEventWithRecord, this,
                                  ['edit_mailing'])
            })
        };
        this.dockedItems = {
            xtype: 'toolbar',
            items: [
                this.actions['new'],
                this.actions['delete'],
                this.actions['edit']
            ]
        }
        this.contextMenu = Ext.create('Ext.menu.Menu', {
            items: [
                this.actions['delete'],
                this.actions['edit']
            ]
        });
        this.callParent(arguments);
        this.addEvents(['new_mailing', 'edit_mailing', 'delete_mailing']);
        this.on('select', this.onRowSelect, this);
        this.on('deselect', this.onRowDeSelect, this);
        this.on('itemcontextmenu', this.onItemCtxMenu, this);
    },
    onRowSelect: function(grid, record) {
        this.selectedRecord = record;
        this._activateObjectActions();
    },
    onRowDeSelect: function(grid, record) {
        this.selectedRecord = null;
        this._deactivateObjectActions();
    },

    onItemCtxMenu: function(grid, record, item, index, ev) {
        this.selectedRecord = record;
        this._activateObjectActions();
        this.contextMenu.showAt(ev.getXY())
        ev.stopEvent();
        return false;
    },

    _activateObjectActions: function() {
        this.actions['edit'].enable();
        this.actions['delete'].enable();
    },

    _deactivateObjectActions: function() {
        this.actions['edit'].disable();
        this.actions['delete'].disable();
    },


    fireEventWithRecord: function(evname) {
        this.fireEvent(evname, this, this.selectedRecord);
    }
});
