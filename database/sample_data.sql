-- Sample Data for T&D Asset Investment Planning System
-- 50 realistic T&D assets with failure modes and condition data

-- ============================================================================
-- 1. ASSET TYPES (T&D-specific taxonomy)
-- ============================================================================

INSERT INTO asset_types (id, category, name, description, voltage_classes, typical_lifespan_years) VALUES
('11111111-1111-1111-1111-111111111111', 'TRANSFORMER', 'Power Transformer', 'Oil-immersed power transformer for transmission and distribution', ARRAY['69kV', '138kV', '230kV', '345kV'], 40),
('22222222-2222-2222-2222-222222222222', 'TRANSFORMER', 'Distribution Transformer', 'Pad-mounted or pole-mounted distribution transformer', ARRAY['12kV', '24kV', '34.5kV'], 35),
('33333333-3333-3333-3333-333333333333', 'BREAKER', 'SF6 Circuit Breaker', 'SF6 gas-insulated high voltage circuit breaker', ARRAY['69kV', '138kV', '230kV'], 35),
('44444444-4444-4444-4444-444444444444', 'BREAKER', 'Vacuum Circuit Breaker', 'Vacuum interrupter circuit breaker for distribution', ARRAY['12kV', '24kV', '34.5kV'], 30),
('55555555-5555-5555-5555-555555555555', 'LINE', 'Overhead Transmission Line', 'Overhead conductor transmission line', ARRAY['69kV', '138kV', '230kV', '345kV'], 50),
('66666666-6666-6666-6666-666666666666', 'LINE', 'Underground Distribution Cable', 'XLPE insulated underground distribution cable', ARRAY['12kV', '24kV', '34.5kV'], 40),
('77777777-7777-7777-7777-777777777777', 'SWITCH', 'Air-Break Switch', 'High voltage air-break disconnect switch', ARRAY['69kV', '138kV'], 35),
('88888888-8888-8888-8888-888888888888', 'SWITCH', 'Load Break Switch', 'Load break switch for distribution feeders', ARRAY['12kV', '24kV', '34.5kV'], 30),
('99999999-9999-9999-9999-999999999999', 'REGULATOR', 'Voltage Regulator', 'Step voltage regulator for distribution', ARRAY['12kV', '24kV'], 30),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'CAPACITOR', 'Shunt Capacitor Bank', 'Shunt capacitor bank for reactive power compensation', ARRAY['12kV', '69kV', '138kV'], 25),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'RECLOSER', 'Automatic Recloser', 'Automatic circuit recloser for overhead distribution', ARRAY['12kV', '24kV'], 25),
('cccccccc-cccc-cccc-cccc-cccccccccccc', 'SECTIONALIZER', 'Line Sectionalizer', 'Automatic line sectionalizer', ARRAY['12kV', '24kV'], 25);

-- ============================================================================
-- 2. ASSET LOCATIONS (Substations and service territories)
-- ============================================================================

INSERT INTO asset_locations (id, substation_id, substation_name, latitude, longitude, voltage_level, service_territory, climate_zone) VALUES
('a1111111-1111-1111-1111-111111111111', 'SUB-001', 'Northside Substation', 40.7589, -73.9851, '138kV', 'North Metro', 'Temperate'),
('a2222222-2222-2222-2222-222222222222', 'SUB-002', 'Westside Substation', 40.7505, -73.9934, '138kV', 'West Metro', 'Temperate'),
('a3333333-3333-3333-3333-333333333333', 'SUB-003', 'Eastside Substation', 40.7614, -73.9776, '138kV', 'East Metro', 'Temperate'),
('a4444444-4444-4444-4444-444444444444', 'SUB-004', 'Southside Substation', 40.7484, -73.9967, '69kV', 'South Metro', 'Temperate'),
('a5555555-5555-5555-5555-555555555555', 'SUB-005', 'Industrial Park Substation', 40.6892, -74.0445, '230kV', 'Industrial District', 'Temperate'),
('a6666666-6666-6666-6666-666666666666', 'SUB-006', 'Riverside Substation', 40.7282, -73.7949, '69kV', 'Riverside', 'Temperate-Humid'),
('a7777777-7777-7777-7777-777777777777', 'SUB-007', 'Hilltop Substation', 40.8176, -73.9782, '138kV', 'Uptown', 'Temperate'),
('a8888888-8888-8888-8888-888888888888', 'SUB-008', 'Valley Substation', 40.6782, -73.9442, '69kV', 'Downtown', 'Temperate'),
('a9999999-9999-9999-9999-999999999999', 'SUB-009', 'Airport Substation', 40.6413, -73.7781, '138kV', 'Airport Zone', 'Coastal'),
('aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'SUB-010', 'Medical Center Substation', 40.7420, -73.9745, '69kV', 'Medical District', 'Temperate');

UPDATE asset_locations SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);

-- ============================================================================
-- 3. ASSETS (50 T&D assets)
-- ============================================================================

INSERT INTO assets (id, asset_type_id, location_id, name, manufacturer, model, serial_number, install_date, mva_rating, voltage_primary_kv, voltage_secondary_kv, health_score, criticality, status) VALUES
-- Transformers (15 units)
('b1111111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-111111111111', 'a1111111-1111-1111-1111-111111111111', 'TX-N-001', 'ABB', 'TRE-138-69-60', 'SN-1998-001', '1998-03-15', 60.0, 138.0, 69.0, 0.72, 5, 'IN_SERVICE'),
('b1111112-1111-1111-1111-111111111112', '11111111-1111-1111-1111-111111111111', 'a2222222-2222-2222-2222-222222222222', 'TX-W-001', 'Siemens', 'GST-138-69-75', 'SN-2002-045', '2002-07-22', 75.0, 138.0, 69.0, 0.85, 5, 'IN_SERVICE'),
('b1111113-1111-1111-1111-111111111113', '11111111-1111-1111-1111-111111111111', 'a3333333-3333-3333-3333-333333333333', 'TX-E-001', 'GE', 'PowerStar-138-69-50', 'SN-1995-112', '1995-11-08', 50.0, 138.0, 69.0, 0.58, 4, 'IN_SERVICE'),
('b1111114-1111-1111-1111-111111111114', '11111111-1111-1111-1111-111111111111', 'a5555555-5555-5555-5555-555555555555', 'TX-IP-001', 'Mitsubishi', 'MT-230-138-150', 'SN-2010-089', '2010-05-12', 150.0, 230.0, 138.0, 0.92, 5, 'IN_SERVICE'),
('b1111115-1111-1111-1111-111111111115', '11111111-1111-1111-1111-111111111111', 'a7777777-7777-7777-7777-777777777777', 'TX-HT-001', 'Hyundai', 'HPT-138-69-40', 'SN-2005-034', '2005-09-30', 40.0, 138.0, 69.0, 0.78, 4, 'IN_SERVICE'),
('b1111116-1111-1111-1111-111111111116', '22222222-2222-2222-2222-222222222222', 'a1111111-1111-1111-1111-111111111111', 'DT-N-001', 'ABB', 'DT-12-0.4-1000', 'SN-2008-201', '2008-04-18', 1.0, 12.0, 0.4, 0.88, 3, 'IN_SERVICE'),
('b1111117-1111-1111-1111-111111111117', '22222222-2222-2222-2222-222222222222', 'a2222222-2222-2222-2222-222222222222', 'DT-W-001', 'Siemens', 'DT-12-0.4-1500', 'SN-2012-156', '2012-02-14', 1.5, 12.0, 0.4, 0.95, 3, 'IN_SERVICE'),
('b1111118-1111-1111-1111-111111111118', '22222222-2222-2222-2222-222222222222', 'a4444444-4444-4444-4444-444444444444', 'DT-S-001', 'GE', 'DT-24-0.4-2000', 'SN-1999-078', '1999-06-22', 2.0, 24.0, 0.4, 0.65, 4, 'IN_SERVICE'),
('b1111119-1111-1111-1111-111111111119', '22222222-2222-2222-2222-222222222222', 'a6666666-6666-6666-6666-666666666666', 'DT-R-001', 'ABB', 'DT-12-0.4-750', 'SN-2001-145', '2001-08-05', 0.75, 12.0, 0.4, 0.71, 3, 'IN_SERVICE'),
('b1111120-1111-1111-1111-111111111120', '22222222-2222-2222-2222-222222222222', 'a8888888-8888-8888-8888-888888888888', 'DT-V-001', 'Schneider', 'DT-34-0.4-2500', 'SN-2015-089', '2015-03-28', 2.5, 34.5, 0.4, 0.96, 4, 'IN_SERVICE'),
('b1111121-1111-1111-1111-111111111121', '11111111-1111-1111-1111-111111111111', 'a9999999-9999-9999-9999-999999999999', 'TX-AIR-001', 'Siemens', 'GST-138-69-100', 'SN-2018-034', '2018-11-15', 100.0, 138.0, 69.0, 0.98, 5, 'IN_SERVICE'),
('b1111122-1111-1111-1111-111111111122', '11111111-1111-1111-1111-111111111111', 'aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'TX-MED-001', 'ABB', 'TRE-69-12-30', 'SN-2003-067', '2003-04-12', 30.0, 69.0, 12.0, 0.74, 5, 'IN_SERVICE'),
('b1111123-1111-1111-1111-111111111123', '22222222-2222-2222-2222-222222222222', 'a1111111-1111-1111-1111-111111111111', 'DT-N-002', 'GE', 'DT-12-0.4-500', 'SN-1990-234', '1990-09-20', 0.5, 12.0, 0.4, 0.42, 3, 'IN_SERVICE'),
('b1111124-1111-1111-1111-111111111124', '22222222-2222-2222-2222-222222222222', 'a3333333-3333-3333-3333-333333333333', 'DT-E-002', 'ABB', 'DT-12-0.4-1000', 'SN-2006-189', '2006-07-08', 1.0, 12.0, 0.4, 0.81, 3, 'IN_SERVICE'),
('b1111125-1111-1111-1111-111111111125', '11111111-1111-1111-1111-111111111111', 'a4444444-4444-4444-4444-444444444444', 'TX-S-002', 'Hyundai', 'HPT-69-12-20', 'SN-1997-156', '1997-12-03', 20.0, 69.0, 12.0, 0.55, 4, 'IN_SERVICE'),

-- Circuit Breakers (12 units)
('c1111111-1111-1111-1111-111111111111', '33333333-3333-3333-3333-333333333333', 'a1111111-1111-1111-1111-111111111111', 'CB-N-001', 'ABB', 'HPL-138-40', 'SN-2000-045', '2000-05-18', NULL, 138.0, NULL, 0.76, 5, 'IN_SERVICE'),
('c1111112-1111-1111-1111-111111111112', '33333333-3333-3333-3333-333333333333', 'a2222222-2222-2222-2222-222222222222', 'CB-W-001', 'Siemens', '3AP1-FG-138', 'SN-2004-078', '2004-09-12', NULL, 138.0, NULL, 0.84, 5, 'IN_SERVICE'),
('c1111113-1111-1111-1111-111111111113', '33333333-3333-3333-3333-333333333333', 'a3333333-3333-3333-3333-333333333333', 'CB-E-001', 'Alstom', 'GL-138-50', 'SN-1998-123', '1998-03-22', NULL, 138.0, NULL, 0.68, 4, 'IN_SERVICE'),
('c1111114-1111-1111-1111-111111111114', '33333333-3333-3333-3333-333333333333', 'a5555555-5555-5555-5555-555555555555', 'CB-IP-001', 'Mitsubishi', 'S1-230-63', 'SN-2012-056', '2012-11-08', NULL, 230.0, NULL, 0.91, 5, 'IN_SERVICE'),
('c1111115-1111-1111-1111-111111111115', '44444444-4444-4444-4444-444444444444', 'a1111111-1111-1111-1111-111111111111', 'VCB-N-001', 'Eaton', 'VCP-W-12', 'SN-2010-134', '2010-06-15', NULL, 12.0, NULL, 0.89, 4, 'IN_SERVICE'),
('c1111116-1111-1111-1111-111111111116', '44444444-4444-4444-4444-444444444444', 'a4444444-4444-4444-4444-444444444444', 'VCB-S-001', 'Schneider', 'HVX-24', 'SN-2016-089', '2016-02-28', NULL, 24.0, NULL, 0.94, 4, 'IN_SERVICE'),
('c1111117-1111-1111-1111-111111111117', '33333333-3333-3333-3333-333333333333', 'a7777777-7777-7777-7777-777777777777', 'CB-HT-001', 'ABB', 'HPL-138-40', 'SN-2006-167', '2006-08-14', NULL, 138.0, NULL, 0.82, 4, 'IN_SERVICE'),
('c1111118-1111-1111-1111-111111111118', '44444444-4444-4444-4444-444444444444', 'a8888888-8888-8888-8888-888888888888', 'VCB-V-001', 'Siemens', '3AH3-12', 'SN-2019-045', '2019-05-20', NULL, 12.0, NULL, 0.97, 3, 'IN_SERVICE'),
('c1111119-1111-1111-1111-111111111119', '33333333-3333-3333-3333-333333333333', 'a9999999-9999-9999-9999-999999999999', 'CB-AIR-001', 'Siemens', '3AP1-FG-138', 'SN-2017-078', '2017-10-12', NULL, 138.0, NULL, 0.95, 5, 'IN_SERVICE'),
('c1111120-1111-1111-1111-111111111120', '44444444-4444-4444-4444-444444444444', 'aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'VCB-MED-001', 'Eaton', 'VCP-W-12', 'SN-2008-156', '2008-04-05', NULL, 12.0, NULL, 0.79, 5, 'IN_SERVICE'),
('c1111121-1111-1111-1111-111111111121', '33333333-3333-3333-3333-333333333333', 'a4444444-4444-4444-4444-444444444444', 'CB-S-002', 'ABB', 'HPL-69-25', 'SN-1995-089', '1995-07-30', NULL, 69.0, NULL, 0.52, 4, 'IN_SERVICE'),
('c1111122-1111-1111-1111-111111111122', '44444444-4444-4444-4444-444444444444', 'a6666666-6666-6666-6666-666666666666', 'VCB-R-001', 'Schneider', 'HVX-12', 'SN-2013-234', '2013-09-18', NULL, 12.0, NULL, 0.87, 3, 'IN_SERVICE'),

-- Lines (10 units)
('d1111111-1111-1111-1111-111111111111', '55555555-5555-5555-5555-555555555555', NULL, 'TL-NW-138-001', 'N/A', 'ACSR-795', 'LINE-1995-001', '1995-04-12', 120.0, 138.0, NULL, 0.71, 5, 'IN_SERVICE'),
('d1111112-1111-1111-1111-111111111112', '55555555-5555-5555-5555-555555555555', NULL, 'TL-ES-138-001', 'N/A', 'ACSR-636', 'LINE-1998-045', '1998-08-22', 100.0, 138.0, NULL, 0.68, 4, 'IN_SERVICE'),
('d1111113-1111-1111-1111-111111111113', '55555555-5555-5555-5555-555555555555', NULL, 'TL-IP-230-001', 'N/A', 'ACSS-1272', 'LINE-2005-089', '2005-06-15', 400.0, 230.0, NULL, 0.84, 5, 'IN_SERVICE'),
('d1111114-1111-1111-1111-111111111114', '66666666-6666-6666-6666-666666666666', NULL, 'UD-N-12-001', 'N/A', 'XLPE-500', 'CABLE-2010-034', '2010-03-28', 10.0, 12.0, NULL, 0.91, 3, 'IN_SERVICE'),
('d1111115-1111-1111-1111-111111111115', '66666666-6666-6666-6666-666666666666', NULL, 'UD-W-12-001', 'N/A', 'XLPE-750', 'CABLE-2015-067', '2015-11-12', 15.0, 12.0, NULL, 0.96, 3, 'IN_SERVICE'),
('d1111116-1111-1111-1111-111111111116', '55555555-5555-5555-5555-555555555555', NULL, 'TL-HT-138-001', 'N/A', 'ACSR-477', 'LINE-1988-123', '1988-09-05', 80.0, 138.0, NULL, 0.48, 4, 'IN_SERVICE'),
('d1111117-1111-1111-1111-111111111117', '66666666-6666-6666-6666-666666666666', NULL, 'UD-S-24-001', 'N/A', 'XLPE-1000', 'CABLE-2008-156', '2008-07-20', 25.0, 24.0, NULL, 0.86, 4, 'IN_SERVICE'),
('d1111118-1111-1111-1111-111111111118', '55555555-5555-5555-5555-555555555555', NULL, 'TL-AIR-138-001', 'N/A', 'ACSR-795', 'LINE-2018-078', '2018-05-15', 120.0, 138.0, NULL, 0.98, 5, 'IN_SERVICE'),
('d1111119-1111-1111-1111-111111111119', '66666666-6666-6666-6666-666666666666', NULL, 'UD-MED-12-001', 'N/A', 'XLPE-500', 'CABLE-2002-189', '2002-12-10', 10.0, 12.0, NULL, 0.74, 5, 'IN_SERVICE'),
('d1111120-1111-1111-1111-111111111120', '55555555-5555-5555-5555-555555555555', NULL, 'TL-V-69-001', 'N/A', 'ACSR-336', 'LINE-1992-234', '1992-02-18', 50.0, 69.0, NULL, 0.55, 3, 'IN_SERVICE'),

-- Switches (8 units)
('e1111111-1111-1111-1111-111111111111', '77777777-7777-7777-7777-777777777777', 'a1111111-1111-1111-1111-111111111111', 'ABS-N-001', 'S&C', 'PMH-9', 'SN-2003-045', '2003-06-12', NULL, 138.0, NULL, 0.78, 4, 'IN_SERVICE'),
('e1111112-1111-1111-1111-111111111112', '77777777-7777-7777-7777-777777777777', 'a2222222-2222-2222-2222-222222222222', 'ABS-W-001', 'Southern States', 'Type LLS', 'SN-2007-078', '2007-09-28', NULL, 138.0, NULL, 0.85, 4, 'IN_SERVICE'),
('e1111113-1111-1111-1111-111111111113', '88888888-8888-8888-8888-888888888888', 'a4444444-4444-4444-4444-444444444444', 'LBS-S-001', 'S&C', 'Omni-Rupter', 'SN-2012-134', '2012-04-15', NULL, 24.0, NULL, 0.92, 3, 'IN_SERVICE'),
('e1111114-1111-1111-1111-111111111114', '88888888-8888-8888-8888-888888888888', 'a6666666-6666-6666-6666-666666666666', 'LBS-R-001', 'ABB', 'SDO', 'SN-2016-089', '2016-08-22', NULL, 12.0, NULL, 0.88, 3, 'IN_SERVICE'),
('e1111115-1111-1111-1111-111111111115', '77777777-7777-7777-7777-777777777777', 'a5555555-5555-5555-5555-555555555555', 'ABS-IP-001', 'S&C', 'PMH-11', 'SN-2010-156', '2010-11-05', NULL, 230.0, NULL, 0.90, 5, 'IN_SERVICE'),
('e1111116-1111-1111-1111-111111111116', '88888888-8888-8888-8888-888888888888', 'a8888888-8888-8888-8888-888888888888', 'LBS-V-001', 'Eaton', 'VFI', 'SN-2019-045', '2019-03-18', NULL, 12.0, NULL, 0.97, 3, 'IN_SERVICE'),
('e1111117-1111-1111-1111-111111111117', '77777777-7777-7777-7777-777777777777', 'a7777777-7777-7777-7777-777777777777', 'ABS-HT-001', 'Southern States', 'Type LLS-II', 'SN-1999-234', '1999-07-30', NULL, 138.0, NULL, 0.62, 4, 'IN_SERVICE'),
('e1111118-1111-1111-1111-111111111118', '88888888-8888-8888-8888-888888888888', 'aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'LBS-MED-001', 'S&C', 'Omni-Rupter', 'SN-2005-189', '2005-05-12', NULL, 12.0, NULL, 0.81, 4, 'IN_SERVICE'),

-- Other equipment (5 units)
('f1111111-1111-1111-1111-111111111111', '99999999-9999-9999-9999-999999999999', 'a4444444-4444-4444-4444-444444444444', 'VR-S-001', 'Siemens', 'SVR-24-10', 'SN-2008-078', '2008-09-15', 10.0, 24.0, NULL, 0.83, 3, 'IN_SERVICE'),
('f1111112-1111-1111-1111-111111111112', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'a1111111-1111-1111-1111-111111111111', 'SC-N-001', 'ABB', 'Cap-12-5.4', 'SN-2014-045', '2014-06-22', 5.4, 12.0, NULL, 0.94, 3, 'IN_SERVICE'),
('f1111113-1111-1111-1111-111111111113', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'a6666666-6666-6666-6666-666666666666', 'REC-R-001', 'S&C', '6801-12', 'SN-2011-134', '2011-03-08', NULL, 12.0, NULL, 0.87, 3, 'IN_SERVICE'),
('f1111114-1111-1111-1111-111111111114', 'cccccccc-cccc-cccc-cccc-cccccccccccc', 'a8888888-8888-8888-8888-888888888888', 'SEC-V-001', 'G&W', 'LCR-12', 'SN-2017-089', '2017-11-28', NULL, 12.0, NULL, 0.91, 2, 'IN_SERVICE'),
('f1111115-1111-1111-1111-111111111115', '99999999-9999-9999-9999-999999999999', 'a3333333-3333-3333-3333-333333333333', 'VR-E-001', 'Beckwith', 'M-6275', 'SN-2004-156', '2004-07-14', 7.5, 12.0, NULL, 0.76, 3, 'IN_SERVICE');

-- ============================================================================
-- 4. FAILURE MODES (T&D-specific failure mechanisms)
-- ============================================================================

INSERT INTO failure_modes (id, asset_type_id, failure_category, mechanism, description, typical_causes, precursors, failure_rate_base, repair_cost_avg, replacement_cost_avg, outage_hours_avg, safety_risk, environmental_risk) VALUES
-- Transformer failure modes
('f2111111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-111111111111', 'CATASTROPHIC', 'Oil Degradation', 'Insulating oil breakdown leading to dielectric failure', ARRAY['Moisture ingress', 'Acid buildup', 'Oxidation', 'Thermal stress'], ARRAY['High acidity', 'Low IFT', 'Dark oil color', 'Increased moisture'], 0.002, 50000.00, 800000.00, 72.0, 3, 4),
('f2111112-1111-1111-1111-111111111112', '11111111-1111-1111-1111-111111111111', 'CATASTROPHIC', 'Winding Failure', 'Turn-to-turn or phase-to-phase insulation failure in windings', ARRAY['Thermal aging', 'Moisture', 'Overloading', 'Lightning surge'], ARRAY['High DGA key gases', 'Increased PD', 'Abnormal sounds', 'Hot spots'], 0.0015, 150000.00, 1200000.00, 168.0, 4, 3),
('f2111113-1111-1111-1111-111111111113', '11111111-1111-1111-1111-111111111111', 'MAJOR', 'Bushing Failure', 'Porcelain or composite bushing flashover or oil leak', ARRAY['Contamination', 'Cracking', 'Seal failure', 'Animal contact'], ARRAY['High PD levels', 'Oil leaks', 'Tracking marks', 'Corona noise'], 0.003, 25000.00, 15000.00, 24.0, 3, 2),
('f2111114-1111-1111-1111-111111111114', '11111111-1111-1111-1111-111111111111', 'MAJOR', 'Tap Changer Failure', 'OLTC mechanism or contact failure', ARRAY['Mechanical wear', 'Contact erosion', 'Oil contamination', 'Motor failure'], ARRAY['Slow operation', 'Contact wear', 'DGA acetylene', 'Irregular sounds'], 0.004, 40000.00, 80000.00, 48.0, 2, 2),
('f2111115-1111-1111-1111-111111111115', '11111111-1111-1111-1111-111111111111', 'MAJOR', 'Core Failure', 'Core insulation failure or core hot spot', ARRAY['Ground fault', 'Insulation aging', 'Foreign object', 'Manufacturing defect'], ARRAY['High core ground current', 'Hot spots', 'DGA hydrogen', 'Vibration'], 0.0008, 100000.00, 800000.00, 120.0, 3, 3),
('f2111116-1111-1111-1111-111111111116', '11111111-1111-1111-1111-111111111111', 'DEGRADED', 'Tank/Pipe Leak', 'Oil leak from tank welds, pipes, or fittings', ARRAY['Corrosion', 'Vibration fatigue', 'Thermal cycling', 'Seal aging'], ARRAY['Oil seepage', 'Low oil level', 'Rust stains', 'Oil puddles'], 0.01, 8000.00, 0.00, 8.0, 1, 4),

-- Circuit Breaker failure modes
('f2222221-2222-2222-2222-222222222221', '33333333-3333-3333-3333-333333333333', 'CATASTROPHIC', 'SF6 Gas Loss', 'Loss of SF6 insulating gas leading to dielectric failure', ARRAY['Seal degradation', 'Porosity', 'Mechanical damage', 'Corrosion'], ARRAY['Low pressure alarm', 'Gas detector alarm', 'Visible leaks'], 0.0025, 30000.00, 500000.00, 48.0, 4, 5),
('f2222222-2222-2222-2222-222222222222', '33333333-3333-3333-3333-333333333333', 'MAJOR', 'Mechanism Failure', 'Operating mechanism failure preventing proper operation', ARRAY['Spring fatigue', 'Motor failure', 'Control circuit fault', 'Lubrication breakdown'], ARRAY['Slow operation', 'Failure to close/open', 'Motor running continuously'], 0.005, 20000.00, 150000.00, 24.0, 3, 1),
('f2222223-2222-2222-2222-222222222223', '33333333-3333-3333-3333-333333333333', 'MAJOR', 'Contact Wear', 'Main contact erosion or welding', ARRAY['Interrupting duty', 'High currents', 'Frequent operations', 'Misalignment'], ARRAY['High contact resistance', 'Excessive heating', 'Abnormal wear patterns'], 0.003, 35000.00, 100000.00, 36.0, 2, 1),
('f2222224-2222-2222-2222-222222222224', '44444444-4444-4444-4444-444444444444', 'MAJOR', 'Vacuum Bottle Failure', 'Loss of vacuum in interrupter bottle', ARRAY['Mechanical shock', 'Manufacturing defect', 'Age', 'Overvoltage'], ARRAY['High contact resistance', 'Visual discharge', 'X-ray emission'], 0.001, 15000.00, 80000.00, 16.0, 3, 1),
('f2222225-2222-2222-2222-222222222225', '44444444-4444-4444-4444-444444444444', 'DEGRADED', 'Control Circuit Failure', 'Secondary control or protection circuit malfunction', ARRAY['Component aging', 'Moisture', 'Vibration', 'Rodent damage'], ARRAY['Relay alarms', 'Indication errors', 'Communication loss'], 0.008, 5000.00, 25000.00, 8.0, 2, 1),

-- Line failure modes
('f2333331-3333-3333-3333-333333333331', '55555555-5555-5555-5555-555555555555', 'CATASTROPHIC', 'Conductor Failure', 'Conductor break or damage causing outage', ARRAY['Fatigue', 'Corrosion', 'Galloping', 'Ice loading', 'Vehicle contact'], ARRAY['Sagging', 'Broken strands', 'Arc marks', 'Vibration damage'], 0.004, 50000.00, 200000.00, 24.0, 3, 2),
('f2333332-3333-3333-3333-333333333332', '55555555-5555-5555-5555-555555555555', 'MAJOR', 'Insulator Failure', 'Porcelain or composite insulator flashover or damage', ARRAY['Contamination', 'Lightning', 'Material defect', 'Gunshot damage'], ARRAY['Tracking', 'Chipped porcelain', 'Corona noise', 'Flashover marks'], 0.006, 15000.00, 80000.00, 12.0, 2, 1),
('f2333333-3333-3333-3333-333333333333', '55555555-5555-5555-5555-555555555555', 'MAJOR', 'Tower/Pole Failure', 'Structural failure of support structure', ARRAY['Corrosion', 'Foundation failure', 'Vehicle impact', 'Wind/ice loading'], ARRAY['Leaning', 'Corrosion', 'Cracks', 'Guy wire issues'], 0.002, 80000.00, 150000.00, 48.0, 4, 2),
('f2333334-3333-3333-3333-333333333334', '66666666-6666-6666-6666-666666666666', 'CATASTROPHIC', 'Cable Insulation Failure', 'XLPE insulation breakdown in underground cable', ARRAY['Water treeing', 'Thermal aging', 'Manufacturing defect', 'Mechanical damage'], ARRAY['Partial discharge', 'High tan delta', 'Sheath damage'], 0.0015, 100000.00, 300000.00, 72.0, 3, 3),
('f2333335-3333-3333-3333-333333333335', '66666666-6666-6666-6666-666666666666', 'MAJOR', 'Cable Joint Failure', 'Failure of cable splice or termination', ARRAY['Installation error', 'Moisture ingress', 'Thermal cycling', 'Material aging'], ARRAY['Hot spots', 'PD activity', 'Oil leaks (fluid)'], 0.003, 40000.00, 100000.00, 36.0, 3, 2),

-- Switch failure modes
('f2444441-4444-4444-4444-444444444441', '77777777-7777-7777-7777-777777777777', 'MAJOR', 'Contact Deterioration', 'Switch contact heating or erosion', ARRAY['Oxidation', 'High currents', 'Frequent switching', 'Misalignment'], ARRAY['Hot spots', 'High resistance', 'Arcing'], 0.004, 12000.00, 60000.00, 16.0, 2, 1),
('f2444442-4444-4444-4444-444444444442', '77777777-7777-7777-7777-777777777777', 'MAJOR', 'Mechanism Binding', 'Operating mechanism jamming or binding', ARRAY['Corrosion', 'Lack of lubrication', 'Misalignment', 'Ice buildup'], ARRAY['Hard to operate', 'Incomplete closing', 'Unusual noise'], 0.005, 8000.00, 45000.00, 12.0, 2, 1),
('f2444443-4444-4444-4444-444444444443', '88888888-8888-8888-8888-888888888888', 'DEGRADED', 'Insulation Tracking', 'Surface tracking on insulation', ARRAY['Contamination', 'Moisture', 'UV degradation', 'Electrical stress'], ARRAY['Carbon tracks', 'Surface discharge', 'Reduced withstand'], 0.006, 5000.00, 25000.00, 8.0, 2, 1);

-- ============================================================================
-- 5. DEGRADATION MODELS (Physics-based, NOT age-based)
-- ============================================================================

INSERT INTO degradation_models (id, failure_mode_id, model_type, weibull_shape, weibull_scale, weibull_location, arrhenius_pre_exp, arrhenius_activation_ev, temp_reference_c, condition_thresholds, model_equation, calibration_data_source, validation_status) VALUES
-- Weibull models for time-to-failure
('g3111111-1111-1111-1111-111111111111', 'f2111111-1111-1111-1111-111111111111', 'WEIBULL', 2.5, 35.0, 5.0, NULL, NULL, NULL, '{"poor": 0.3, "fair": 0.5, "good": 0.7, "excellent": 0.9}'::jsonb, 'R(t) = exp(-((t-γ)/η)^β)', 'IEEE C57.106', 'VALIDATED'),
('g3111112-1111-1111-1111-111111111112', 'f2111112-1111-1111-1111-111111111112', 'WEIBULL', 3.0, 40.0, 8.0, NULL, NULL, NULL, '{"poor": 0.25, "fair": 0.45, "good": 0.65, "excellent": 0.85}'::jsonb, 'R(t) = exp(-((t-γ)/η)^β)', 'EPRI Transformer Guide', 'VALIDATED'),
('g3111113-1111-1111-1111-111111111113', 'f2111113-1111-1111-1111-111111111113', 'WEIBULL', 2.0, 30.0, 3.0, NULL, NULL, NULL, '{"poor": 0.4, "fair": 0.6, "good": 0.8, "excellent": 0.95}'::jsonb, 'R(t) = exp(-((t-γ)/η)^β)', 'Manufacturer data', 'VALIDATED'),
('g3111114-1111-1111-1111-111111111114', 'f2111114-1111-1111-1111-111111111114', 'WEIBULL', 2.8, 25.0, 5.0, NULL, NULL, NULL, '{"poor": 0.35, "fair": 0.55, "good": 0.75, "excellent": 0.9}'::jsonb, 'R(t) = exp(-((t-γ)/η)^β)', 'MR Service data', 'VALIDATED'),

-- Arrhenius thermal aging models
('g3111121-1111-1111-1111-111111111121', 'f2111111-1111-1111-1111-111111111111', 'ARRHENIUS', NULL, NULL, NULL, 1.5e12, 1.1, 110.0, '{"aging_rate_ref": 1.0, "aging_doubling_per_10c": 2.0}'::jsonb, 'k = A * exp(-Ea/kT)', 'IEEE C57.91', 'VALIDATED'),
('g3111122-1111-1111-1111-111111111122', 'f2111112-1111-1111-1111-111111111112', 'ARRHENIUS', NULL, NULL, NULL, 2.0e11, 1.05, 110.0, '{"aging_rate_ref": 1.0, "aging_doubling_per_10c": 1.93}'::jsonb, 'k = A * exp(-Ea/kT)', 'IEEE C57.91', 'VALIDATED'),

-- Breaker degradation models
('g3222221-2222-2222-2222-222222222221', 'f2222221-2222-2222-2222-222222222221', 'WEIBULL', 2.2, 32.0, 5.0, NULL, NULL, NULL, '{"poor": 0.3, "fair": 0.5, "good": 0.7, "excellent": 0.9}'::jsonb, 'R(t) = exp(-((t-γ)/η)^β)', 'CIGRE study', 'VALIDATED'),
('g3222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'WEIBULL', 2.5, 28.0, 3.0, NULL, NULL, NULL, '{"poor": 0.35, "fair": 0.55, "good": 0.75, "excellent": 0.9}'::jsonb, 'R(t) = exp(-((t-γ)/η)^β)', 'EPRI breaker data', 'VALIDATED'),

-- Line degradation models
('g3333331-3333-3333-3333-333333333331', 'f2333331-3333-3333-3333-333333333331', 'WEIBULL', 1.8, 45.0, 10.0, NULL, NULL, NULL, '{"poor": 0.25, "fair": 0.45, "good": 0.65, "excellent": 0.85}'::jsonb, 'R(t) = exp(-((t-γ)/η)^β)', 'NERC data', 'VALIDATED'),
('g3333332-3333-3333-3333-333333333332', 'f2333332-3333-3333-3333-333333333332', 'WEIBULL', 2.0, 35.0, 5.0, NULL, NULL, NULL, '{"poor": 0.3, "fair": 0.5, "good": 0.7, "excellent": 0.9}'::jsonb, 'R(t) = exp(-((t-γ)/η)^β)', 'Field experience', 'VALIDATED'),
('g3333334-3333-3333-3333-333333333334', 'f2333334-3333-3333-3333-333333333334', 'ARRHENIUS', NULL, NULL, NULL, 5.0e10, 0.95, 90.0, '{"aging_rate_ref": 1.0, "aging_doubling_per_10c": 1.8}'::jsonb, 'k = A * exp(-Ea/kT)', 'Cable aging studies', 'VALIDATED');

-- ============================================================================
-- 6. NETWORK NODES (Topology)
-- ============================================================================

INSERT INTO network_nodes (id, asset_id, node_type, name, voltage_level, operational_state, latitude, longitude) VALUES
('n1111111-1111-1111-1111-111111111111', 'b1111111-1111-1111-1111-111111111111', 'BUS', 'N-138kV-BUS-1', '138kV', 'ACTIVE', 40.7589, -73.9851),
('n2222222-2222-2222-2222-222222222222', 'b1111112-1111-1111-1111-111111111112', 'BUS', 'W-138kV-BUS-1', '138kV', 'ACTIVE', 40.7505, -73.9934),
('n3333333-3333-3333-3333-333333333333', 'b1111113-1111-1111-1111-111111111113', 'BUS', 'E-138kV-BUS-1', '138kV', 'ACTIVE', 40.7614, -73.9776),
('n4444444-4444-4444-4444-444444444444', 'b1111115-1111-1111-1111-111111111115', 'BUS', 'HT-138kV-BUS-1', '138kV', 'ACTIVE', 40.8176, -73.9782),
('n5555555-5555-5555-5555-555555555555', 'b1111114-1111-1111-1111-111111111114', 'BUS', 'IP-230kV-BUS-1', '230kV', 'ACTIVE', 40.6892, -74.0445),
('n6666666-6666-6666-6666-666666666666', NULL, 'JUNCTION', 'J-NW-138-001', '138kV', 'ACTIVE', 40.7547, -73.9893),
('n7777777-7777-7777-7777-777777777777', NULL, 'JUNCTION', 'J-ES-138-001', '138kV', 'ACTIVE', 40.7559, -73.9815),
('n8888888-8888-8888-8888-888888888888', 'b1111121-1111-1111-1111-111111111121', 'BUS', 'AIR-138kV-BUS-1', '138kV', 'ACTIVE', 40.6413, -73.7781),
('n9999999-9999-9999-9999-999999999999', 'b1111122-1111-1111-1111-111111111122', 'BUS', 'MED-69kV-BUS-1', '69kV', 'ACTIVE', 40.7420, -73.9745);

UPDATE network_nodes SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);

-- ============================================================================
-- 7. NETWORK EDGES (Connectivity)
-- ============================================================================

INSERT INTO network_edges (id, from_node_id, to_node_id, asset_id, edge_type, length_km, impedance_r, impedance_x, thermal_rating_mva, emergency_rating_mva) VALUES
('e5555551-5555-5555-5555-555555555551', 'n1111111-1111-1111-1111-111111111111', 'n6666666-6666-6666-6666-666666666666', 'd1111111-1111-1111-1111-111111111111', 'OVERHEAD', 12.5, 1.25, 4.5, 120.0, 144.0),
('e5555552-5555-5555-5555-555555555552', 'n6666666-6666-6666-6666-666666666666', 'n2222222-2222-2222-2222-222222222222', 'd1111111-1111-1111-1111-111111111111', 'OVERHEAD', 8.3, 0.83, 3.0, 120.0, 144.0),
('e5555553-5555-5555-5555-555555555553', 'n3333333-3333-3333-3333-333333333333', 'n7777777-7777-7777-7777-777777777777', 'd1111112-1111-1111-1111-111111111112', 'OVERHEAD', 15.2, 1.52, 5.5, 100.0, 120.0),
('e5555554-5555-5555-5555-555555555554', 'n7777777-7777-7777-7777-777777777777', 'n4444444-4444-4444-4444-444444444444', 'd1111116-1111-1111-1111-111111111116', 'OVERHEAD', 6.8, 0.68, 2.5, 80.0, 96.0),
('e5555555-5555-5555-5555-555555555555', 'n5555555-5555-5555-5555-555555555555', 'n1111111-1111-1111-1111-111111111111', 'd1111113-1111-1111-1111-111111111113', 'OVERHEAD', 22.0, 1.1, 8.8, 400.0, 480.0),
('e5555556-5555-5555-5555-555555555556', 'n8888888-8888-8888-8888-888888888888', 'n3333333-3333-3333-3333-333333333333', 'd1111118-1111-1111-1111-111111111118', 'OVERHEAD', 18.5, 1.85, 6.8, 120.0, 144.0);

UPDATE network_edges SET geom = ST_MakeLine(
    (SELECT geom FROM network_nodes WHERE id = network_edges.from_node_id),
    (SELECT geom FROM network_nodes WHERE id = network_edges.to_node_id)
);

-- ============================================================================
-- 8. SWITCHING PATHS (Alternative feeds)
-- ============================================================================

INSERT INTO switching_paths (id, source_node_id, target_node_id, path_distance_km, switching_time_min, backup_capacity_mva, automatic_switching, is_active) VALUES
('s6666661-6666-6666-6666-666666666661', 'n1111111-1111-1111-1111-111111111111', 'n2222222-2222-2222-2222-222222222222', 20.8, 15, 100.0, TRUE, TRUE),
('s6666662-6666-6666-6666-666666666662', 'n3333333-3333-3333-3333-333333333333', 'n4444444-4444-4444-4444-444444444444', 22.0, 20, 80.0, FALSE, TRUE),
('s6666663-6666-6666-6666-666666666663', 'n5555555-5555-5555-5555-555555555555', 'n8888888-8888-8888-8888-888888888888', 35.5, 30, 250.0, TRUE, TRUE);

-- ============================================================================
-- 9. CONDITION ASSESSMENTS
-- ============================================================================

INSERT INTO condition_assessments (id, asset_id, assessment_date, assessor, assessment_type, overall_condition, health_index, probability_of_failure, remaining_life_years, next_assessment_due, confidence_score, notes) VALUES
('ca111111-1111-1111-1111-111111111111', 'b1111111-1111-1111-1111-111111111111', '2024-06-15', 'Grid Analytics LLC', 'DIAGNOSTIC', 3, 0.72, 0.028, 12.5, '2025-06-15', 0.85, 'Moderate oil degradation, DGA trending upward'),
('ca111112-1111-1111-1111-111111111112', 'b1111112-1111-1111-1111-111111111112', '2024-05-20', 'Grid Analytics LLC', 'DIAGNOSTIC', 4, 0.85, 0.012, 22.0, '2025-05-20', 0.90, 'Good condition, normal aging'),
('ca111113-1111-1111-1111-111111111113', 'b1111113-1111-1111-1111-111111111113', '2024-04-10', 'Transformer Services Inc', 'DIAGNOSTIC', 2, 0.58, 0.045, 8.0, '2024-10-10', 0.80, 'High acidity, elevated moisture, requires attention'),
('ca111114-1111-1111-1111-111111111114', 'b1111114-1111-1111-1111-111111111114', '2024-08-05', 'Grid Analytics LLC', 'DIAGNOSTIC', 5, 0.92, 0.005, 30.0, '2025-08-05', 0.95, 'Excellent condition, like new'),
('ca111115-1111-1111-1111-111111111115', 'b1111115-1111-1111-1111-111111111115', '2024-07-12', 'Transformer Services Inc', 'DIAGNOSTIC', 3, 0.78, 0.018, 16.0, '2025-07-12', 0.85, 'Minor tap changer wear, otherwise good'),
('ca111121-1111-1111-1111-111111111121', 'b1111121-1111-1111-1111-111111111121', '2024-09-20', 'Grid Analytics LLC', 'DIAGNOSTIC', 5, 0.98, 0.002, 35.0, '2025-09-20', 0.95, 'New installation, excellent condition'),
('ca111123-1111-1111-1111-111111111123', 'b1111123-1111-1111-1111-111111111123', '2024-03-15', 'Field Services Co', 'VISUAL', 1, 0.42, 0.085, 3.5, '2024-09-15', 0.70, 'End of life, significant degradation, replacement recommended'),
('ca211111-1111-1111-1111-111111111111', 'c1111111-1111-1111-1111-111111111111', '2024-06-20', 'Breaker Services Inc', 'DIAGNOSTIC', 3, 0.76, 0.022, 14.0, '2025-06-20', 0.85, 'Normal wear, SF6 pressure stable'),
('ca211113-1111-1111-1111-111111111113', 'c1111113-1111-1111-1111-111111111113', '2024-05-10', 'Breaker Services Inc', 'DIAGNOSTIC', 2, 0.68, 0.035, 10.0, '2024-11-10', 0.80, 'Mechanism showing signs of wear, monitoring recommended'),
('ca211121-1111-1111-1111-111111111121', 'c1111121-1111-1111-1111-111111111121', '2024-02-28', 'Field Services Co', 'DIAGNOSTIC', 1, 0.52, 0.065, 5.0, '2024-08-28', 0.75, 'Aging equipment, multiple issues, replacement planning needed');

-- ============================================================================
-- 10. DIAGNOSTIC TESTS (DGA, oil quality, etc.)
-- ============================================================================

INSERT INTO diagnostic_tests (id, asset_id, test_date, test_type, oil_dielectric_strength, oil_moisture_ppm, oil_acidity, oil_interfacial_tension, dissolved_gases, dga_key_gas, dga_rogers_ratio, insulation_power_factor, winding_resistance, turns_ratio_deviation, temperature_rise, overall_test_result) VALUES
-- Transformer TX-N-001 (moderate condition)
('dt111111-1111-1111-1111-111111111111', 'b1111111-1111-1111-1111-111111111111', '2024-06-15', 'DGA', 38.0, 25, 0.15, 22.0, '{"H2": 150, "CH4": 80, "C2H6": 45, "C2H4": 120, "C2H2": 5, "CO": 350, "CO2": 2800, "total": 750}'::jsonb, 'C2H4', 2, 0.0085, '{"A": 0.245, "B": 0.246, "C": 0.244}'::jsonb, 0.15, 55.0, 'CAUTION'),
('dt111112-1111-1111-1111-111111111112', 'b1111111-1111-1111-1111-111111111111', '2024-06-15', 'OIL_QUALITY', 38.0, 25, 0.15, 22.0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'CAUTION'),

-- Transformer TX-W-001 (good condition)
('dt121111-1111-1111-1111-111111111121', 'b1111112-1111-1111-1111-111111111112', '2024-05-20', 'DGA', 52.0, 12, 0.05, 38.0, '{"H2": 45, "CH4": 25, "C2H6": 15, "C2H4": 30, "C2H2": 0, "CO": 180, "CO2": 1500, "total": 295}'::jsonb, 'C2H4', 0, 0.0035, '{"A": 0.198, "B": 0.199, "C": 0.197}'::jsonb, 0.08, 48.0, 'PASS'),

-- Transformer TX-E-001 (poor condition)
('dt131111-1111-1111-1111-111111111131', 'b1111113-1111-1111-1111-111111111113', '2024-04-10', 'DGA', 28.0, 45, 0.35, 14.0, '{"H2": 450, "CH4": 280, "C2H6": 95, "C2H4": 520, "C2H2": 45, "CO": 850, "CO2": 5200, "total": 2240}'::jsonb, 'C2H4', 6, 0.025, '{"A": 0.312, "B": 0.318, "C": 0.309}'::jsonb, 0.45, 68.0, 'FAIL'),
('dt131112-1111-1111-1111-111111111132', 'b1111113-1111-1111-1111-111111111113', '2024-04-10', 'OIL_QUALITY', 28.0, 45, 0.35, 14.0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'FAIL'),

-- Breaker CB-E-001 (showing wear)
('dt231111-1111-1111-1111-111111111113', 'c1111113-1111-1111-1111-111111111113', '2024-05-10', 'SF6_QUALITY', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'CAUTION');

-- ============================================================================
-- 11. CUSTOMER CONNECTIONS
-- ============================================================================

INSERT INTO customer_connections (id, asset_id, customers_served, critical_customers, peak_load_mw, average_load_mw, hospitals_served, schools_served, emergency_services, water_wastewater_facilities, industrial_mw, commercial_mw, residential_mw, agricultural_mw, avg_outage_cost_per_hour) VALUES
('cc111111-1111-1111-1111-111111111111', 'b1111111-1111-1111-1111-111111111111', 45000, 12, 52.5, 35.0, 2, 8, 3, 1, 15.0, 22.5, 14.0, 1.0, 85000.00),
('cc111112-1111-1111-1111-111111111112', 'b1111112-1111-1111-1111-111111111112', 52000, 8, 68.0, 45.0, 1, 12, 2, 2, 25.0, 28.0, 14.5, 0.5, 92000.00),
('cc111113-1111-1111-1111-111111111113', 'b1111113-1111-1111-1111-111111111113', 38000, 6, 42.0, 28.0, 1, 6, 2, 1, 12.0, 18.0, 11.5, 0.5, 68000.00),
('cc111114-1111-1111-1111-111111111114', 'b1111114-1111-1111-1111-111111111114', 125000, 25, 145.0, 98.0, 3, 20, 5, 3, 65.0, 52.0, 27.0, 1.0, 185000.00),
('cc111115-1111-1111-1111-111111111115', 'b1111115-1111-1111-1111-111111111115', 28000, 4, 35.0, 22.0, 0, 5, 1, 1, 8.0, 15.0, 11.5, 0.5, 52000.00),
('cc111121-1111-1111-1111-111111111121', 'b1111121-1111-1111-1111-111111111121', 85000, 35, 95.0, 62.0, 1, 5, 8, 2, 5.0, 35.0, 54.0, 1.0, 125000.00),
('cc111122-1111-1111-1111-111111111122', 'b1111122-1111-1111-1111-111111111122', 15000, 45, 28.5, 19.0, 4, 2, 12, 1, 2.0, 22.0, 4.0, 0.5, 95000.00),
('cc211111-1111-1111-1111-111111111111', 'c1111111-1111-1111-1111-111111111111', 45000, 12, 52.5, 35.0, 2, 8, 3, 1, 15.0, 22.5, 14.0, 1.0, 85000.00),
('cc311111-1111-1111-1111-111111111111', 'd1111111-1111-1111-1111-111111111111', 72000, 15, 85.0, 58.0, 2, 12, 4, 2, 28.0, 38.0, 18.5, 0.5, 135000.00),
('cc311112-1111-1111-1111-111111111112', 'd1111112-1111-1111-1111-111111111112', 58000, 10, 68.0, 45.0, 1, 10, 3, 1, 22.0, 30.0, 15.5, 0.5, 108000.00);

-- ============================================================================
-- 12. CONSEQUENCE PROFILES (MONETIZED - in $)
-- ============================================================================

INSERT INTO consequence_profiles (id, asset_id, calculation_date, customer_interruption_cost, customer_interruption_cost_hourly, safety_incident_probability, safety_incident_cost, regulatory_fine_probability, regulatory_fine_cost, environmental_remediation_cost, equipment_repair_cost, equipment_replacement_cost, network_reconfiguration_cost, reputation_damage_cost, total_consequence_per_event, annual_expected_consequence, currency) VALUES
-- TX-N-001
('cp111111-1111-1111-1111-111111111111', 'b1111111-1111-1111-1111-111111111111', '2024-06-15', 2850000.00, 85000.00, 0.0005, 250000.00, 0.001, 50000.00, 75000.00, 50000.00, 800000.00, 45000.00, 200000.00, 4075000.00, 114100.00, 'USD'),
-- TX-W-001
('cp111112-1111-1111-1111-111111111112', 'b1111112-1111-1111-1111-111111111112', '2024-05-20', 3080000.00, 92000.00, 0.0003, 150000.00, 0.0008, 40000.00, 50000.00, 50000.00, 950000.00, 40000.00, 150000.00, 4470000.00, 107280.00, 'USD'),
-- TX-E-001 (older, higher risk)
('cp111113-1111-1111-1111-111111111113', 'b1111113-1111-1111-1111-111111111113', '2024-04-10', 2270000.00, 68000.00, 0.0008, 400000.00, 0.002, 100000.00, 100000.00, 150000.00, 1100000.00, 35000.00, 300000.00, 4305000.00, 193725.00, 'USD'),
-- TX-IP-001 (critical industrial)
('cp111114-1111-1111-1111-111111111114', 'b1111114-1111-1111-1111-111111111114', '2024-08-05', 6175000.00, 185000.00, 0.0004, 300000.00, 0.0015, 150000.00, 125000.00, 150000.00, 1800000.00, 75000.00, 500000.00, 9175000.00, 229375.00, 'USD'),
-- TX-HT-001
('cp111115-1111-1111-1111-111111111115', 'b1111115-1111-1111-1111-111111111115', '2024-07-12', 1735000.00, 52000.00, 0.0004, 200000.00, 0.001, 50000.00, 60000.00, 40000.00, 650000.00, 30000.00, 120000.00, 2865000.00, 51570.00, 'USD'),
-- TX-AIR-001 (airport - very critical)
('cp111121-1111-1111-1111-111111111121', 'b1111121-1111-1111-1111-111111111121', '2024-09-20', 4165000.00, 125000.00, 0.0006, 500000.00, 0.002, 250000.00, 100000.00, 100000.00, 1200000.00, 60000.00, 800000.00, 7075000.00, 212250.00, 'USD'),
-- TX-MED-001 (medical district)
('cp111122-1111-1111-1111-111111111122', 'b1111122-1111-1111-1111-111111111122', '2024-03-15', 3165000.00, 95000.00, 0.001, 800000.00, 0.003, 300000.00, 80000.00, 100000.00, 850000.00, 50000.00, 600000.00, 5945000.00, 356700.00, 'USD'),
-- CB-N-001
('cp211111-1111-1111-1111-111111111111', 'c1111111-1111-1111-1111-111111111111', '2024-06-20', 2850000.00, 85000.00, 0.001, 500000.00, 0.001, 50000.00, 250000.00, 30000.00, 500000.00, 25000.00, 150000.00, 4255000.00, 106375.00, 'USD'),
-- Line TL-NW-138-001
('cp311111-1111-1111-1111-111111111111', 'd1111111-1111-1111-1111-111111111111', '2024-06-01', 4500000.00, 135000.00, 0.0008, 400000.00, 0.001, 75000.00, 50000.00, 50000.00, 200000.00, 80000.00, 250000.00, 5605000.00, 156940.00, 'USD');

-- ============================================================================
-- 13. RISK CALCULATIONS
-- ============================================================================

INSERT INTO risk_calculations (id, asset_id, calculation_date, scenario_type, time_horizon_years, annual_failure_probability, cumulative_failure_prob, expected_annual_cost, expected_lifecycle_cost, risk_adjusted_npv, value_at_risk_95, confidence_interval_lower, confidence_interval_upper, key_assumptions, calculation_method) VALUES
-- TX-N-001
('rc111111-1111-1111-1111-111111111111', 'b1111111-1111-1111-1111-111111111111', '2024-06-15', 'BASE_CASE', 10, 0.028, 0.245, 114100.00, 891980.00, 723456.00, 285000.00, 0.022, 0.035, '{"load_factor": 0.65, "ambient_temp": 20, "maintenance_quality": "good"}'::jsonb, 'WEIBULL_ARRHENIUS'),
-- TX-W-001
('rc111112-1111-1111-1111-111111111112', 'b1111112-1111-1111-1111-111111111112', '2024-05-20', 'BASE_CASE', 10, 0.012, 0.113, 53640.00, 419112.00, 385678.00, 225000.00, 0.009, 0.016, '{"load_factor": 0.70, "ambient_temp": 20, "maintenance_quality": "excellent"}'::jsonb, 'WEIBULL_ARRHENIUS'),
-- TX-E-001 (high risk)
('rc111113-1111-1111-1111-111111111113', 'b1111113-1111-1111-1111-111111111113', '2024-04-10', 'BASE_CASE', 10, 0.045, 0.369, 193725.00, 1513050.00, 987654.00, 450000.00, 0.038, 0.053, '{"load_factor": 0.75, "ambient_temp": 22, "maintenance_quality": "fair"}'::jsonb, 'WEIBULL_ARRHENIUS'),
('rc111114-1111-1111-1111-111111111114', 'b1111113-1111-1111-1111-111111111113', '2024-04-10', 'STRESSED', 10, 0.068, 0.498, 292740.00, 2286960.00, 1456789.00, 650000.00, 0.058, 0.079, '{"load_factor": 0.90, "ambient_temp": 30, "maintenance_quality": "poor"}'::jsonb, 'WEIBULL_ARRHENIUS'),
-- TX-IP-001 (industrial critical)
('rc111115-1111-1111-1111-111111111115', 'b1111114-1111-1111-1111-111111111114', '2024-08-05', 'BASE_CASE', 10, 0.008, 0.077, 73400.00, 573320.00, 523456.00, 350000.00, 0.006, 0.011, '{"load_factor": 0.80, "ambient_temp": 25, "maintenance_quality": "excellent"}'::jsonb, 'WEIBULL_ARRHENIUS'),
-- TX-AIR-001
('rc111121-1111-1111-1111-111111111121', 'b1111121-1111-1111-1111-111111111121', '2024-09-20', 'BASE_CASE', 10, 0.005, 0.049, 35375.00, 276325.00, 256789.00, 280000.00, 0.003, 0.008, '{"load_factor": 0.60, "ambient_temp": 18, "maintenance_quality": "excellent"}'::jsonb, 'WEIBULL_ARRHENIUS'),
-- TX-MED-001 (medical - high consequence)
('rc111122-1111-1111-1111-111111111122', 'b1111122-1111-1111-1111-111111111122', '2024-03-15', 'BASE_CASE', 10, 0.035, 0.296, 208075.00, 1624585.00, 1123456.00, 520000.00, 0.029, 0.042, '{"load_factor": 0.72, "ambient_temp": 21, "maintenance_quality": "good"}'::jsonb, 'WEIBULL_ARRHENIUS'),
-- CB-N-001
('rc211111-1111-1111-1111-111111111111', 'c1111111-1111-1111-1111-111111111111', '2024-06-20', 'BASE_CASE', 10, 0.022, 0.198, 93610.00, 730358.00, 598765.00, 320000.00, 0.018, 0.027, '{"operations_per_year": 15, "maintenance_quality": "good"}'::jsonb, 'WEIBULL'),
-- CB-E-001 (showing wear)
('rc211113-1111-1111-1111-111111111113', 'c1111113-1111-1111-1111-111111111113', '2024-05-10', 'BASE_CASE', 10, 0.035, 0.296, 148925.00, 1161615.00, 876543.00, 380000.00, 0.029, 0.042, '{"operations_per_year": 25, "maintenance_quality": "fair"}'::jsonb, 'WEIBULL'),
-- Line TL-NW-138-001
('rc311111-1111-1111-1111-111111111111', 'd1111111-1111-1111-1111-111111111111', '2024-06-01', 'BASE_CASE', 10, 0.028, 0.245, 156940.00, 1222132.00, 987654.00, 420000.00, 0.023, 0.034, '{"wind_exposure": "high", "corrosion_environment": "moderate"}'::jsonb, 'WEIBULL');

-- ============================================================================
-- 14. INTERVENTION OPTIONS
-- ============================================================================

INSERT INTO intervention_options (id, asset_id, intervention_type, description, cost_estimate, cost_uncertainty_percent, implementation_time_months, risk_reduction_percent, failure_probability_reduction, life_extension_years, reliability_improvement_factor, priority_score, benefit_cost_ratio, status) VALUES
-- TX-E-001 (poor condition - needs attention)
('io111113-1111-1111-1111-111111111113', 'b1111113-1111-1111-1111-111111111113', 'REPLACE', 'Replace aging transformer with new 50MVA unit', 1200000.00, 15.0, 6, 95.0, 0.04275, 35.0, 3.5, 8.56, 3.42, 'PROPOSED'),
('io111114-1111-1111-1111-111111111114', 'b1111113-1111-1111-1111-111111111113', 'REFURBISH_MAJOR', 'Major refurbishment: rewind, new bushings, OLTC rebuild', 450000.00, 20.0, 4, 70.0, 0.0315, 15.0, 2.0, 6.72, 2.69, 'PROPOSED'),
('io111115-1111-1111-1111-111111111115', 'b1111113-1111-1111-1111-111111111113', 'MONITOR_ENHANCE', 'Install online DGA monitoring and thermal sensors', 85000.00, 10.0, 2, 25.0, 0.01125, 0.0, 1.3, 5.24, 2.10, 'PROPOSED'),

-- TX-N-001 (moderate condition)
('io111111-1111-1111-1111-111111111111', 'b1111111-1111-1111-1111-111111111111', 'REFURBISH_MINOR', 'Oil reclamation and bushing replacement', 125000.00, 15.0, 2, 45.0, 0.0126, 8.0, 1.5, 6.18, 2.47, 'PROPOSED'),
('io111112-1111-1111-1111-111111111112', 'b1111111-1111-1111-1111-111111111111', 'MONITOR_ENHANCE', 'Enhanced monitoring: online DGA, thermal imaging', 65000.00, 10.0, 1, 20.0, 0.0056, 0.0, 1.2, 4.85, 1.94, 'PROPOSED'),

-- CB-S-002 (aging breaker)
('io211121-1111-1111-1111-111111111121', 'c1111121-1111-1111-1111-111111111121', 'REPLACE', 'Replace with new SF6 breaker', 450000.00, 15.0, 4, 90.0, 0.0585, 30.0, 4.0, 8.92, 3.57, 'PROPOSED'),
('io211122-1111-1111-1111-111111111122', 'c1111121-1111-1111-1111-111111111121', 'MAINTAIN_PREVENTIVE', 'Enhanced preventive maintenance program', 45000.00, 15.0, 1, 35.0, 0.02275, 5.0, 1.4, 5.67, 2.27, 'PROPOSED'),

-- Line TL-HT-138-001 (old line)
('io311116-1111-1111-1111-111111111116', 'd1111116-1111-1111-1111-111111111116', 'REPLACE', 'Reconductoring with high-temperature conductor', 850000.00, 20.0, 8, 85.0, 0.0408, 40.0, 2.5, 7.45, 2.98, 'PROPOSED'),
('io311117-1111-1111-1111-111111111117', 'd1111116-1111-1111-1111-111111111116', 'REFURBISH_MINOR', 'Structure reinforcement and insulator replacement', 280000.00, 15.0, 4, 50.0, 0.024, 15.0, 1.6, 5.89, 2.36, 'PROPOSED');

-- ============================================================================
-- 15. INVESTMENT PROJECTS
-- ============================================================================

INSERT INTO investment_projects (id, project_name, project_type, budget_year, total_budget, risk_reduction_total, implementation_year, completion_year, status, priority_rank, description) VALUES
('pj111111-1111-1111-1111-111111111111', 'TX-E-001 Transformer Replacement', 'ASSET_REPLACEMENT', 2025, 1200000.00, 4305000.00, 2025, 2025, 'PLANNED', 1, 'Replace aging transformer at Eastside Substation'),
('pj111112-1111-1111-1111-111111111112', 'Critical Transformer Monitoring Program', 'RELIABILITY', 2025, 250000.00, 850000.00, 2025, 2025, 'PLANNED', 3, 'Install online monitoring on 5 critical transformers'),
('pj111113-1111-1111-1111-111111111113', 'Aging Breaker Replacement Program', 'ASSET_REPLACEMENT', 2025, 900000.00, 2800000.00, 2025, 2026, 'PLANNED', 2, 'Replace breakers over 25 years old'),
('pj111114-1111-1111-1111-111111111114', 'Hilltop Transmission Line Upgrade', 'ASSET_REPLACEMENT', 2026, 850000.00, 2100000.00, 2026, 2026, 'PLANNED', 4, 'Reconductor aging 138kV line'),
('pj111115-1111-1111-1111-111111111115', 'Substation Monitoring Enhancement', 'MONITORING', 2025, 350000.00, 650000.00, 2025, 2025, 'PLANNED', 5, 'Deploy advanced monitoring across substations');

-- ============================================================================
-- 16. PORTFOLIO SCENARIOS
-- ============================================================================

INSERT INTO portfolio_scenarios (id, scenario_name, budget_constraint, risk_tolerance, time_horizon_years, selected_projects, total_investment, total_risk_reduction, expected_roi, risk_adjusted_return, optimization_date, optimization_method, constraints) VALUES
('ps111111-1111-1111-1111-111111111111', '2025 Base Case Portfolio', 3500000.00, 5000000.00, 10, ARRAY['pj111111-1111-1111-1111-111111111111'::uuid, 'pj111112-1111-1111-1111-111111111112'::uuid, 'pj111113-1111-1111-1111-111111111113'::uuid], 2350000.00, 7955000.00, 3.38, 2.85, '2024-10-15', 'KNAPSACK_GREEDY', '{"min_risk_reduction": 5000000, "max_projects": 10}'::jsonb),
('ps111112-1111-1111-1111-111111111112', '2025 Constrained Budget', 2000000.00, 8000000.00, 10, ARRAY['pj111111-1111-1111-1111-111111111111'::uuid, 'pj111113-1111-1111-1111-111111111113'::uuid], 2100000.00, 7105000.00, 3.38, 2.65, '2024-10-15', 'KNAPSACK_GREEDY', '{"budget_limit": 2000000, "mandatory_projects": ["pj111111-1111-1111-1111-111111111111"]}'::jsonb),
('ps111113-1111-1111-1111-111111111113', '2025 Risk-Averse Portfolio', 5000000.00, 2000000.00, 10, ARRAY['pj111111-1111-1111-1111-111111111111'::uuid, 'pj111112-1111-1111-1111-111111111112'::uuid, 'pj111113-1111-1111-1111-111111111113'::uuid, 'pj111114-1111-1111-1111-111111111114'::uuid, 'pj111115-1111-1111-1111-111111111115'::uuid], 3550000.00, 10505000.00, 2.96, 2.55, '2024-10-15', 'MILP', '{"min_risk_reduction": 8000000, "max_annual_budget": 4000000}'::jsonb);
