const { DataTypes } = require('sequelize');
const sequelize = require('../db/sequelize');

const AE = sequelize.define('ae', {
  ri: { type: DataTypes.STRING(64), primaryKey: true },
  ty: { type: DataTypes.INTEGER, allowNull: false, defaultValue: 2 },
  sid: { type: DataTypes.STRING(255) },
  int_cr: { type: DataTypes.STRING(255) },
  rn: { type: DataTypes.STRING(20), allowNull: false },
  pi: { type: DataTypes.STRING(255) },
  et: { type: DataTypes.STRING(20) },
  ct: { type: DataTypes.STRING(20) },
  lt: { type: DataTypes.STRING(20) },
  acpi: { type: DataTypes.ARRAY(DataTypes.STRING(255)) },
  lbl: { type: DataTypes.ARRAY(DataTypes.STRING(255)) },
  cr: { type: DataTypes.STRING(255) },
  api: { type: DataTypes.STRING(255) },
  apn: { type: DataTypes.STRING(255) },
  aei: { type: DataTypes.STRING(255) },
  poa: { type: DataTypes.ARRAY(DataTypes.STRING(255)) },
  rr: { type: DataTypes.BOOLEAN, allowNull: false },
  srv: { type: DataTypes.ARRAY(DataTypes.STRING(10)) },
  csz: { type: DataTypes.ARRAY(DataTypes.STRING(10)) },
  loc: { type: DataTypes.GEOMETRY('GEOMETRY', 4326) },
}, {
  tableName: 'ae',
  timestamps: false,
});

module.exports = AE;