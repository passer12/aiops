//暂时无用的文件
export const NodeService = {
    getTreeNodesData() {
        return fetch('/demo/data/treenodes.json')
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                console.log(data);
                return data.root;
            });
    },

    getTreeTableNodesData() {
        return [
            {
                key: '0',
                data: {
                    name: 'Applications',
                    size: '100kb',
                    type: 'Folder'
                }
            }
        ];
    },

    getTreeTableNodes() {
        return Promise.resolve(this.getTreeTableNodesData());
    },

    getTreeNodes() {
        return Promise.resolve(this.getTreeNodesData());
    }
};
