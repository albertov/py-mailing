Ext.define('WebMailing.controller.Categories', {
    extend: 'Ext.app.Controller',
    views: ['category.Panel'],
    refs: [
        {
            ref: 'panel',
            selector: 'categories'
        }
    ],

    init: function() {
        this.control({
            "categories": {
                render: this.onPanelRender
            },
            "category_tree": {
                new_item: this.onNewCategory,
                delete_item: this.onDeleteCategory
            }
        });
    },
    onPanelRender: function(panel) {
        var store = Ext.getStore('Categories');
        panel.loadMask.bindStore(store);
        if (store.getCount()==0) {
            store.load();
        }
    },
    onNewCategory: function(tree, parent) {
        var item = parent.appendChild({
            title: 'Sin título', //i18n
            category_id: parent.isRoot()?null:parent.getId()
        });
        parent.expand();
        tree.rowEditor.startEdit(item, 0);
    },
    onDeleteCategory: function(tree, record) {
        Ext.Msg.confirm(
            "Aviso",
            Ext.String.format(
                'Se borrara permanentemente "{0}". <strong>TODAS</strong> '+
                'las subcategorias se eliminarán también. '+
                 '¿Seguro?',
                 record.get('title')),
            Ext.bind(this._confirmDeleteHandler, this, [record], 0)
        );
    },
    _confirmDeleteHandler: function(record, btn) {
        if (btn=="yes") {
            record.remove(true);
        }
    },
});
