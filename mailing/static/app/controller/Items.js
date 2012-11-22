Ext.define('Mailing.controller.Items', {
    extend: 'Ext.app.Controller',
    views: ['item.Tree'],
    models: ['Item'],
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
                itemmove: this.onItemMove,
                beforedrop: this.onTreeBeforeDrop
            }

        });
        this._delayedUpdate = new Ext.util.DelayedTask(
            this.updateItemPositionsAndCategories, this);
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
        for (var i=0; i<data.records.length; i++) {
            var model = data.records[i], allow;
            if (!model.isLeaf()) {
                // Si es una carpeta solo permitir moverla antes o despues de otra
                // en el mismo nivel
                allow = (!overModel.isLeaf() &&
                         model.parentNode===overModel.parentNode && 
                         (dropPosition=="before" || dropPosition=="after"));
            } else {
                // Si es un item solo permitir moverlo dentro de la misma carpeta
                // o a otra que no sea la raiz
                allow = (overModel.isLeaf() || 
                         (!overModel.isRoot() && dropPosition=='append') ||
                         (!overModel.isRoot() && !overModel.parentNode.isRoot()  &&
                          (dropPosition=="before" || dropPosition=="after")))
            }

            if (!allow) {
                return false;
            }

        }
    },
    onNewItem: function(tree, node) {
        var parent = node.get('record'),
            category_id = parent?parent.get('id'):null;
            store = tree.store.items,
            item = store.add({
                id: null,
                title: 'Sin título', // i18n
                content: 'Texto', // i18n
                category_id: category_id,
                type: 'Article'
            })[0];
        store.on('write', function() {
            this.selectNodeForItem(item);
        }, this, {single:true, delay:1});
    },
    selectNodeForItem: function(item) {
        var tree = this.getTree(),
            root = tree.getRootNode(),
            node = root.findChild("id", "item-"+item.get('id'), true);
        tree.getSelectionModel().select(node);
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
    onItemMove: function() {
        this._delayedUpdate.delay(10);
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
