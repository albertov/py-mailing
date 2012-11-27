Ext.define('Mailing.ComboGrid', {
    extend: 'Ext.form.ComboBox',
    requires: [
        'Ext.grid.Panel',
        'Ext.toolbar.Paging'
    ],
    alias: ['combogrid'],

    gridClass: 'Ext.grid.Panel',


    // copied from ComboBox 
    createPicker: function() {
        var me = this,
        picker,
        menuCls = Ext.baseCSSPrefix + 'menu',
        opts = Ext.apply({
            selModel: {
                mode: me.multiSelect ? 'SIMPLE' : 'SINGLE'
            },
            floating: true,
            hidden: true,
            ownerCt: me.ownerCt,
            cls: me.el.up('.' + menuCls) ? menuCls : '',
            store: me.store,
            displayField: me.displayField,
            focusOnToFront: false,
            pageSize: me.pageSize,
            dockedItems: [{
                xtype: 'pagingtoolbar',
                store: me.store,
                dock: 'bottom',
                displayInfo: true
            }]
        }, me.listConfig, me.defaultListConfig);

        picker = me.picker = Ext.create(this.gridClass, opts);


        // hack: pass getNode() to the view
        picker.getNode = function() {
            picker.getView().getNode(arguments);
        };


        me.mon(picker.getView(), {
            refresh: me.onListRefresh,
            scope:me
        });
        me.mon(picker, {
            itemclick: me.onItemClick,
//            refresh: me.onListRefresh,
            scope: me
        });


        me.mon(picker.getSelectionModel(), {
            selectionChange: me.onListSelectionChange,
            scope: me
        });

        return picker;
    }
});
        
