const path = require('path');
const webpack = require('webpack');
const merge = require('webpack-merge');
const util = require('util');

const CleanPlugin = require('clean-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');
const BundleTrackerPlugin = require('webpack-bundle-tracker');

const __merge_rules__ = {
    'module.rules.use': 'replace'
}


let common = {
    context: __dirname,

    entry: {
        main: './static/scpc/js/main.js',
        vendor: ['jquery', 'popper.js', 'bootstrap']
    },

    output: {
        path: path.resolve(__dirname, 'static/bundles'),
        publicPath: '/static/bundles/',
        filename: '[name].[chunkhash].js'
    },

    resolve: {
        modules: [
            path.resolve(__dirname, 'static/scpc/js'),
            'node_modules'
        ]
    },

    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['env'],
                        plugins: ['transform-object-rest-spread']
                    }
                }
            },
            {
                test: /\.scss$/,
                use: [
                    'style-loader',
                    {
                        loader: 'css-loader',
                        options: {
                            importLoaders: 1
                        }
                    },
                    'postcss-loader',
                    'sass-loader',
                ]
            },
            {
                test: /\.(png|jpg|gif)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name].[ext]'
                        }
                    }
                ]
            },
            {
                test: /\.(eot|otf|ttf|woff|woff2|svg)(\?.*$|$)/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name].[ext]'
                        }
                    }
                ]
            }
        ]
    },

    plugins: [
        // Dynamically create common (lib) and vendor chunks in one go.
        // See ~webpack/examples/common-chunk-and-vendor-chunk for an
        // explanation of how this works.
        new webpack.optimize.CommonsChunkPlugin({
            name: ['common', 'vendor'],  // Order is important
            minChunks: 2,
        }),

        // Extract the Webpack runtime into it's own chunk. This can
        // use any name that isn't also the name of an entry chunk.
        new webpack.optimize.CommonsChunkPlugin({
            name: ['runtime'],
        }),

        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            Popper: ['popper.js', 'default']
        }),

        new BundleTrackerPlugin({
            path: __dirname,
            filename: 'static/webpack-stats.json',
            indent: 4
        }),

        // Required for backwards-compatibility with v1 loaders
        new webpack.LoaderOptionsPlugin({
            debug: process.env.NODE_ENV == 'development'
        })
    ]
};


if (process.env.NODE_ENV === 'development') {
    module.exports = merge.smartStrategy(__merge_rules__)(common, {
        output: {
            publicPath: 'http://localhost:8080/bundles/',
            filename: '[name].js'  // hashing isn't allowed with HMR
        },

        plugins: [
            // In production we rely on extract-text-webpack-plugin to
            // consolidate all CSS inlined by the style-loader into a
            // dedicated file. In development, however, an empty file must
            // be created manually (by copying) to prevent client imports
            // from failing.
            new CopyPlugin([
                {from: 'static/scpc/css/main.css', to: 'main.css'}
            ]),

            new webpack.HotModuleReplacementPlugin(),
            new webpack.NamedModulesPlugin()
        ],

        devServer: {
            hot: true,
            compress: true,
            overlay: true,
            publicPath: 'http://localhost:8080/bundles/',
            contentBase: [
                path.resolve(__dirname, 'static'),
                path.resolve(__dirname, 'static_collected'), // Wagtail assets
            ],
            watchOptions: {
                ignored: /node_modules/
            },
            proxy: {
                // Files served from ${contentBase} are always served from
                // "/", regardless of ${publicPath} (see
                // https://github.com/webpack/webpack-dev-server/issues/954)
                // A workaround is to also serve bundles from "/" (via
                // ${publicPath}) and proxy/rewrite client "/static" requests
                // to "/".
                '/static': {
                    target: 'http://localhost:8080/',
                    pathRewrite: { '^/static': '' }
                }
            },
            headers: {
                // Allow cross-origin requests for Wagtail assets (e.g. fonts)
                'Access-Control-Allow-Origin': 'http://localhost:8000'
            }
        }
    });
}


if (process.env.NODE_ENV === 'production' || !process.env.NODE_ENV) {
    module.exports = merge.smartStrategy(__merge_rules__)(common, {
        module: {
            rules: [
                {
                    test: /\.scss$/,
                    use: ExtractTextPlugin.extract({
                        use: [
                            {
                                loader: 'css-loader',
                                options: {
                                    minimize: 'true',
                                    importLoaders: 1
                                }
                            },
                            'postcss-loader',
                            'sass-loader'
                        ],
                        fallback: 'style-loader'
                    })
                },
                {
                    test: /\.(png|jpg|gif)$/,
                    use: [
                        {
                            loader: 'file-loader',
                            options: {
                                name: '[hash].[ext]'
                            }
                        }
                    ]
                },
                {
                    test: /\.(eot|otf|ttf|woff|woff2|svg)(\?.*$|$)/,
                    use: [
                        {
                            loader: 'file-loader',
                            options: {
                                name: '[hash].[ext]'
                            }
                        }
                    ]
                }
            ]
        },

        plugins: [
            new CleanPlugin(['static/bundles']),

            // See https://github.com/webpack/webpack/issues/1315
            new webpack.NamedModulesPlugin(),
            new webpack.NamedChunksPlugin(),

            new ExtractTextPlugin('main.[contenthash].css'),

            new webpack.optimize.UglifyJsPlugin({
                mange: {
                    except: [
                        '$', 'jquery', 'Popper', '$super', 'exports', 'require'
                    ]
                }
            })
        ]
    });
}
