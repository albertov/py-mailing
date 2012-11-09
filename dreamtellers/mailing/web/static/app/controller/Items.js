Ext.define('WebMailing.controller.Items', {
    extend: 'Ext.app.Controller',
    views: ['item.Tree'],
    refs: [
        {
            ref: 'tree',
            selector: 'item_tree'
        }, {
            ref: 'form',
            selector: 'item_form'
        }
    ],
    controllers: ['Categories'],
    init: function() {
        this.control({
            item_tree: {
                select: this.onEditNode,
                itemremove: Ext.bind(this.setActiveRecord, this, [null]),
                new_item: this.onNewItem,
                delete_item: this.onDeleteNode,
                edit_item: this.onEditNode,
                itemmove: this.updateItemPositionsAndCategories,
                beforedrop: this.onTreeBeforeDrop
            }

        });
    },
    setActiveRecord: function(record) {
        if (record!==null) {
            this.getForm().loadRecord(record);
        } else {
            this.getForm().disable();
        }
    },
    onEditNode: function(tree, node) {
        if (node.isItem()) {
            var record = node.get('record');
            if (record) {
                this.setActiveRecord(record);
            }
        } else {
            this.setActiveRecord(null);
        }
    },
    onTreeBeforeDrop: function(node, data, overModel, dropPosition) {
        var model = data.records[0];
        console.debug('onTreeBeforeDrop', model.get('title'),
                      overModel.get('title'), dropPosition);
        if (!model.isLeaf()) {
            // Si es una carpeta solo permitir moverla antes o despues de otra
            // en el mismo nivel
            return (!overModel.isLeaf() &&
                    model.parentNode===overModel.parentNode && 
                    (dropPosition=="before" || dropPosition=="after"));
        } else {
            // Si es un item solo permitir moverlo dentro de la misma carpeta
            // o a otra que no sea la raiz
            return (overModel.isLeaf() || 
                    (!overModel.isRoot() && dropPosition=='append') ||
                    (!overModel.isRoot() && !overModel.parentNode.isRoot()  &&
                     (dropPosition=="before" || dropPosition=="after")))
        }
    },
    onNewItem: function(tree, node) {
        console.debug('onNewItem', arguments);
        var parent = node.get('record'),
            category_id = parent?parent.get('id'):null;
            item = tree.store.items.add({
                id: null,
                title: 'Sin título', // i18n
                content: 'Texto', // i18n
                category_id: category_id,
                type: 'Article'
            })[0];
            this.setActiveRecord(item);
    },
    onDeleteNode: function(tree, node) {
        var record = node.get('record');
        if (record) {
            Ext.Msg.confirm(
                "Aviso",
                Ext.String.format('Se borrara permanentemente "{0}". ¿Seguro?',
                                  record.get('title')),
                Ext.bind(this._confirmDeleteHandler, this, [record], 0)
            );
        }
    },
    _confirmDeleteHandler: function(record, btn) {
        if (btn=="yes") {
            record.store.remove(record);
        }
    },
    updateItemPositionsAndCategories: function() {
        var pos=0;
        var treeStore = this.getTree().getStore();
        treeStore.items.suspendAutoSync();
        treeStore.getRootNode().cascadeBy(function(n) {
            if (n.isItem()) {
                n.get('record').set('position', pos++);
                var cat = n.parentNode.get('record');
                n.get('record').set('category_id', cat?cat.getId():null);
            }
        });
        treeStore.items.resumeAutoSync();
        treeStore.items.sync();
    }
});
