Ext.define('WebMailing.controller.Items', {
    extend: 'Ext.app.Controller',
    views: ['item.Tree'],
    refs: [
        {
            ref: 'tree',
            selector: 'item_tree'
        }
    ],
    controllers: ['Categories'],
    init: function() {
        this.control({
            "item_tree": {
                new_category: this.onNewCategory,
                new_item: this.onNewItem,
                delete_node: this.onDeleteNode,
                edit_node: this.onEditNode
            }
        });
    },
    onNewCategory: function(tree, node) {
        var parent = node.get('record');
        if (!parent) {
            var store=Ext.getStore('Categories');
            parent=store.getRootNode();
        }
        var category = parent.appendChild({
            title: 'Sin título', //i18n
            category_id:parent?parent.get('id'):null
        });

    },
    onNewItem: function(tree, node) {
        var parent = node.get('record');
        var item = tree.store.items.add({
            id: null,
            title: 'Sin título',
            category_id:parent?parent.get('id'):null
        });
        console.debug('onNewItem,', item);
    },
    onDeleteNode: function(tree, node) {
        var record = node.get('record');
        if(!record)
            return;
        Ext.Msg.confirm(
            "Aviso",
            Ext.String.format('Se borrara permanentemente "{0}". ¿Seguro?',
                              record.get('title')),
            Ext.bind(this._confirmDeleteHandler, this, [record], 0)
        );
    },
    _confirmDeleteHandler: function(record, btn) {
        if (btn=="yes") {
            record.store.remove(record);
        }
    },

    onEditNode: function(tree, node) {
        console.debug('onEditNode', node.get('record'));
    }
});
