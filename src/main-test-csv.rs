// 基础的图表分析
// 读取本地配置，上传 测试v，.xls等文件
use serde_derive::{Serialize, Deserialize};
use std::fmt;
// use toml::Table;
slint::include_modules!();

#[derive(Debug, Serialize, Deserialize)]

use polars::prelude::*;

struct BaseConfig {
    dir: String,
    file_ext: String,
    sate: bool,
    count: i64,
}

impl ::std::default::Default for BaseConfig {
    fn default() -> Self { Self { dir: "local".into(), 
                                  file_ext: "test".into(),
                                  sate: true,
                                  count: 100} }
}




// 加载本地 toml 配置
// fn load_default_conf()-> Result<(), confy::ConfyError> {

//     let config: Config = toml::from_str(r#"
//     let config: Config = toml::from_str(r#"
//    ip = '127.0.0.1'

//    [keys]
//    github = 'xxxxxxxxxxxxxxxxx'
//    travis = 'yyyyyyyyyyyyyyyyy'
// "#).unwrap();

// assert_eq!(config.ip, "127.0.0.1");
// assert_eq!(config.port, None);
// assert_eq!(config.keys.github, "xxxxxxxxxxxxxxxxx");
// assert_eq!(config.keys.travis.as_ref().unwrap(), "yyyyyyyyyyyyyyyyy");
// }

mod smbc { // 方法1： 使用 include!
    include!("./smbc.rs");
}

fn main() -> Result<(), confy::ConfyError>  {
    
    // let s = Series::new("a", &[1, 2, 3, 4, 5]);
    // println!("{}", s);

    let cfg: BaseConfig = confy::load("my_app", "local")?;
    println!("Defautl config: {:#?}", cfg);
    
    // let update_cfg = BaseConfig {
    //     dir: "new".into(), 
    //     file_ext: ".txt".into(),
    //     sate: true,
    //     count: 1000
    // };
    // // 更新配置
    // confy::store("my_app", "local", update_cfg)?;
    // println!("Updated config: {:#?}", cfg);
    // 更新窗口
    // AppWindow::new().unwrap().run().unwrap();
    smbc::upload();
    Ok(())

}

